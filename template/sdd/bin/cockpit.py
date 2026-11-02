#!/usr/bin/env python3
"""The cockpit's Python part, run by sdd/bin/cockpit: the report, and opencode's usage, whose logs are a SQLite base.

`opencode <repo> <since> <until>` prints the tokens opencode spent in <repo> between two epoch seconds, as
`sdd/bin/cockpit usage` does. Without a window, `report` and `hints <repo> <state> <quiz journal>` read the commit times
of the dev's agent batches on their input, and look at the last 10.
"""
import glob
import json
import os
import re
import sqlite3
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from types import SimpleNamespace

FIELDS = ["input", "output", "cache_read", "cache_write"]
REVIEW = re.compile(r"review|quiz", re.I)
# Anthropic's price ratios, in input tokens: a cache read costs a tenth, a cache write 1.25 (2 when kept an hour),
# an output token 5.
READ, WRITE, WRITE_HOUR, OUTPUT = 0.1, 1.25, 2, 5
# Text runs about 3.5 characters a token; an image about 1600 tokens.
CHARS_PER_TOKEN, IMAGE = 3.5, 1600
# The dev's last batches, whatever their pace: enough that "never called" means something, and a hint comes back
# after as many.
BATCHES = 10
# A hint names what costs at least this share, below which a cut does not show on the bill, or a context this long.
SHARE, LONG = 0.05, 150_000


def main():
    if sys.argv[1:2] == ["report"] and len(sys.argv) in (3, 5):
        end = int(sys.argv[4]) if len(sys.argv) == 5 else int(time.time())
        start = int(sys.argv[3]) if len(sys.argv) == 5 else window(batches())[0]
        report(sys.argv[2], start, end)
    elif sys.argv[1:2] == ["hints"] and len(sys.argv) == 5:
        hints(sys.argv[2], sys.argv[3], sys.argv[4], batches())
    elif sys.argv[1:2] == ["opencode"] and len(sys.argv) == 5:
        usage(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        sys.exit("usage: bash sdd/bin/cockpit report <repo> [<since> <until>] | hints | usage <repo> <since> <until>")


def usage(repo, start, end):
    rows = defaultdict(lambda: dict.fromkeys(["calls"] + FIELDS, 0))
    for (role, model), tokens in opencode(repo, start, end):
        row = rows[role, family(model)]
        row["calls"] += 1
        for field in FIELDS:
            row[field] += tokens[field]
    for key in sorted(rows):
        print("\t".join(list(key) + [str(rows[key][field]) for field in ["calls"] + FIELDS]))


def measure(repo, start, end):
    """Claude Code's calls in a window: exact sums by role and model, the contexts they start with and reach, then
    estimates of what is sent along. Also each tool ever called, and the size of each plugin's skills in the listing."""
    seen = SimpleNamespace(roles=defaultdict(lambda: [0, 0]), starts=defaultdict(list), sources=Counter(),
                           called=Counter(), listing={}, total=0, reads=0, longest=(0, 0))
    for path, role in claude_logs(repo):
        calls = 0
        for context, cost, read, model, opening in trace(path, start, end, seen):
            seen.roles[role, family(model)][0] += 1
            seen.roles[role, family(model)][1] += cost
            seen.total, seen.reads, calls = seen.total + cost, seen.reads + read, calls + 1
            seen.longest = max(seen.longest, (context, calls))
            if opening:
                seen.starts["session" if role == "writer" else "sub-agent"].append(context)
    return seen


def report(repo, start, end):
    """Where the tokens went, for the dev to cut."""
    seen = measure(repo, start, end)
    roles, starts, sources, total, reads, longest = (seen.roles, seen.starts, seen.sources, seen.total, seen.reads,
                                                     seen.longest)
    if not total:
        sys.exit(f"No Claude Code log of {repo} in that window.")
    print(f"Claude Code in {repo}: {short(total)} input-equivalent tokens (cache read x{READ}, cache write x{WRITE}"
          f" or x{WRITE_HOUR}, output x{OUTPUT}).\n")
    print(f"{'role':24}{'model':10}{'calls':>7}{'tokens':>9}{'share':>7}")
    for (role, model), (calls, cost) in sorted(roles.items(), key=lambda item: -item[1][1]):
        print(f"{role:24}{model:10}{calls:>7}{short(cost):>9}{cost / total:>7.0%}")
    print()
    for kind, contexts in starts.items():
        median = short(statistics.median(contexts))
        print(f"A {kind} starts with {median} tokens of context (median of {len(contexts)}).")
    print(f"The longest reached {short(longest[0])} after {longest[1]} calls; cache reads are {reads / total:.0%} of"
          f" the cost.\n")
    print("Estimated from their size, what is sent along with the calls:")
    for source, cost in sources.most_common(8):
        print(f"{source[:40]:41}{short(cost):>9}{cost / total:>7.0%}")


def batches():
    """The commit times of the dev's agent batches, newest first, as sdd/bin/cockpit gives them."""
    return [int(when) for when in sys.stdin.read().split()]


def window(times):
    """Where the last BATCHES batches start, the start of the logs when there are fewer, and how many they are."""
    return (times[BATCHES] if len(times) > BATCHES else 0), max(min(len(times), BATCHES), 1)


def hints(repo, state, journal, times):
    """What the last batches show to cut or to write down, for the agent to put to the dev as a question. Silent before
    the first batch and when nothing is new: a hint shown comes back BATCHES batches later at the earliest."""
    if not times:
        return
    start, count = window(times)
    found = cuts(measure(repo, start, int(time.time())), count)
    for module, flags in sorted(flagged(journal, start).items()):
        if flags >= 2:
            found["quiz " + module] = (f"Quiz answers in {module} were flagged unclear or not what you wanted {flags}"
                                       f" times: propose the rule you would write.")
    shown = {}
    if os.path.exists(state):
        with open(state) as file:
            shown = {key: int(batch) for key, batch in (line.rstrip("\n").split("\t") for line in file)}
    for key, text in found.items():
        if len(times) - shown.get(key, -BATCHES) >= BATCHES:
            print("HINT " + text)
            shown[key] = len(times)
    os.makedirs(os.path.dirname(state) or ".", exist_ok=True)
    with open(state, "w") as file:
        file.writelines(f"{key}\t{batch}\n" for key, batch in shown.items())


def cuts(seen, count):
    """What the logs show to cut, by kind."""
    found = {}
    if not seen.total:
        return found
    servers = [source[len("MCP instructions "):] for source in seen.sources if source.startswith("MCP instructions ")]
    # Claude Code names a server's tools mcp__<server>__<tool>, its name's other signs turned to "_".
    unused = [server for server in servers if not any(
        tool.startswith(f"mcp__{re.sub(r'[^A-Za-z0-9_-]', '_', server)}__") for tool in seen.called)]
    if unused:
        cost = sum(seen.sources["MCP instructions " + server] for server in unused)
        found["mcp"] = (f"MCP servers never called in this repo's logs, whose instructions cost {short(cost / count)}"
                        f" tokens a batch: {', '.join(sorted(unused))}.")
    listing = seen.sources["skill listing"]
    idle = {plugin: size for plugin, size in seen.listing.items() if seen.called["skill " + plugin] == 0}
    if listing >= SHARE * seen.total and idle:
        found["skills"] = (f"The skill listing costs {short(listing / count)} tokens a batch"
                           f" ({listing / seen.total:.0%}); plugins whose skills were never called here make"
                           f" {sum(idle.values()) / sum(seen.listing.values()):.0%} of it, the largest:"
                           f" {', '.join(sorted(idle, key=idle.get, reverse=True)[:5])}.")
    for source, cost in seen.sources.items():
        if cost >= SHARE * seen.total and source != "skill listing" and not source.startswith("MCP"):
            found[source] = (f"{source[0].upper()}{source[1:]} cost {short(cost / count)} tokens a batch"
                             f" ({cost / seen.total:.0%}), sent again with every later call.")
    if seen.longest[0] > LONG:
        found["context"] = (f"A log reached {short(seen.longest[0])} tokens of context, read again with each call: a"
                            f" fresh session per batch reads less.")
    return found


def flagged(journal, start):
    """Per module, the quiz answers flagged unclear or not wanted since start, once per title and cause: a commit that
    fails after the quiz passed journals it again."""
    flags = set()
    if os.path.exists(journal):
        with open(journal) as file:
            for line in file:
                fields = line.rstrip("\n").split("\t")
                if fields[0] == "v2" and int(fields[1]) > start:
                    flags.update((module, fields[4], cause) for module in fields[2].split(",") if module != "-"
                                 for cause in fields[3].split(",") if cause in ("unclear", "not-wanted"))
    return Counter(module for module, _, _ in flags)


def trace(path, start, end, seen):
    """Each reply of a log in the window, as its context, cost, cache read cost, model, and whether it opens the log.
    Adds to seen.sources what each piece sent along costs: written once, then read again with every later call until a
    compaction drops it."""
    live, pending, names, replies = Counter(), Counter(), {}, set()
    for entry in entries(path):
        if entry.get("subtype") == "compact_boundary":
            live.clear()
        message = entry.get("message") or {}
        if reply(message, replies):
            use = message["usage"]
            write = WRITE_HOUR if (use.get("cache_creation") or {}).get("ephemeral_1h_input_tokens") else WRITE
            if start < epoch(entry["timestamp"]) <= end:
                read = READ * use.get("cache_read_input_tokens", 0)
                for source, size in live.items():
                    seen.sources[source] += READ * size
                for source, size in pending.items():
                    seen.sources[source] += write * size
                context = sum(use.get(f, 0) for f in ["input_tokens", "cache_creation_input_tokens",
                                                       "cache_read_input_tokens"])
                cost = use.get("input_tokens", 0) + write * use.get("cache_creation_input_tokens", 0) + read
                yield context, cost + OUTPUT * use.get("output_tokens", 0), read, message["model"], len(replies) == 1
            live.update(pending)
            pending.clear()
        for source, size in pieces(entry, names, seen):
            pending[source] += size


def pieces(entry, names, seen):
    """What an entry sends along with the next calls, other than the conversation, as (source, estimated tokens).
    Notes in seen each tool called, and each plugin's share of the skill listing."""
    attachment = entry.get("attachment") or {}
    kind = attachment.get("type")
    if kind == "skill_listing":
        sizes = Counter()
        for line in attachment.get("content", "").splitlines():
            sizes[plugin(line[2:].split(": ")[0])] += len(line)
        # The largest listing a plugin had: a later one may only add skills.
        for name, size in sizes.items():
            seen.listing[name] = max(seen.listing.get(name, 0), size)
        yield "skill listing", tokens(attachment.get("content", ""))
    elif kind == "hook_additional_context":
        yield f"hook {attachment.get('hookEvent')}", tokens(str(attachment.get("content", "")))
    elif kind == "mcp_instructions_delta":
        for name, block in zip(attachment.get("addedNames", []), attachment.get("addedBlocks", [])):
            yield f"MCP instructions {name}", tokens(block)
    elif kind in ("instructions", "nested_memory"):
        yield "memory files (CLAUDE.md, AGENTS.md)", tokens(json.dumps(attachment))
    content = (entry.get("message") or {}).get("content")
    for block in content if isinstance(content, list) else []:
        if block.get("type") == "tool_use":
            names[block["id"]] = block["name"]
            seen.called[block["name"]] += 1
            if block["name"] == "Skill":
                seen.called["skill " + plugin((block.get("input") or {}).get("skill", ""))] += 1
        elif block.get("type") == "tool_result":
            # One line per MCP server, not per tool.
            name = re.sub(r"^(mcp__[^_]+(?:_[^_]+)*?)__.*", r"\1", names.get(block.get("tool_use_id"), "?"))
            yield f"tool results {name}", tokens(block.get("content"))


def plugin(skill):
    """code-review for code-review:review; a skill of no plugin is its own."""
    return skill.split(":")[0]


def tokens(content):
    if isinstance(content, list):
        return sum(IMAGE if part.get("type") == "image" else tokens(part.get("text", "")) for part in content)
    return len(content or "") / CHARS_PER_TOKEN


def short(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.1f}k" if n >= 1e3 else f"{n:.0f}"


def claude_logs(repo):
    """Claude Code keeps a JSONL per session under the repo's path, and one per sub-agent next to a .meta.json."""
    home = os.environ.get("CLAUDE_CONFIG_DIR", os.path.expanduser("~/.claude"))
    folder = os.path.join(home, "projects", re.sub(r"[^A-Za-z0-9]", "-", repo))
    for path in glob.glob(f"{folder}/*.jsonl") + glob.glob(f"{folder}/*/subagents/*.jsonl"):
        role = "writer"
        if os.path.basename(os.path.dirname(path)) == "subagents":
            meta = read_json(path[: -len(".jsonl")] + ".meta.json")
            role = "reviewer" if REVIEW.search(meta.get("description", "")) else "agent:" + meta.get("agentType", "")
        yield path, role


def reply(message, seen):
    """Whether a message is a model reply not yet seen: a reply is logged once per content block, with one usage."""
    if "usage" not in message or message.get("id") in seen or message.get("model") == "<synthetic>":
        return False
    seen.add(message.get("id"))
    return True


def opencode(repo, start, end):
    """opencode keeps every message in one SQLite base; a sub-agent runs in a child session."""
    share = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    base = os.path.join(share, "opencode", "opencode.db")
    if not os.path.exists(base):
        return []
    db = sqlite3.connect(f"file:{base}?mode=ro", uri=True)
    found = []
    for data, parent, title in db.execute(
        "select m.data, s.parent_id, s.title from message m join session s on s.id = m.session_id"
        " where s.directory = ? and m.time_created > ? and m.time_created <= ?", (repo, start * 1000, end * 1000)
    ):
        message = json.loads(data)
        if message.get("role") != "assistant":
            continue
        tokens = message.get("tokens", {})
        found.append(((opencode_role(parent, title, message), message["modelID"]), {
            "input": tokens.get("input", 0),
            # Claude Code counts thinking in its output, opencode apart: output includes reasoning in both.
            "output": tokens.get("output", 0) + tokens.get("reasoning", 0),
            "cache_read": tokens.get("cache", {}).get("read", 0),
            "cache_write": tokens.get("cache", {}).get("write", 0),
        }))
    return found


def opencode_role(parent, title, message):
    if not parent:
        return "writer"
    return "reviewer" if REVIEW.search(title or "") else "agent:" + message["agent"]


def family(model):
    """claude-opus-5-5 is opus: the shared ledger need not tell apart who runs which version."""
    match = re.search(r"opus|sonnet|haiku|fable", model)
    return match.group() if match else model


def entries(path):
    """The entries of a JSONL log. A session still running may hold a half-written last line."""
    with open(path, encoding="utf-8") as log:
        for line in log:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                pass


def epoch(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp()


def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path) as file:
        return json.load(file)


main()
