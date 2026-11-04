"""Claude Code keeps a JSONL log per session under the repo's path, and one per sub-agent next to a .meta.json."""
import calendar
import glob
import json
import os
import re
import time
from collections import Counter

from fabrik.logs import REVIEW

# Anthropic's price ratios, in input tokens: a cache read costs a tenth, a cache write 1.25 (2 when kept an hour),
# an output token 5.
READ, WRITE, WRITE_HOUR, OUTPUT = 0.1, 1.25, 2, 5
# Text runs about 3.5 characters a token; an image about 1600 tokens.
CHARS_PER_TOKEN, IMAGE = 3.5, 1600


def usage(repo, start, end):
    seen = set()
    for path, role in logs(repo):
        for entry in entries(path):
            message = entry.get("message") or {}
            if reply(message, seen) and start < epoch(entry["timestamp"]) <= end:
                use = message["usage"]
                yield role, message["model"], {
                    "input": use.get("input_tokens", 0),
                    "output": use.get("output_tokens", 0),
                    "cache_read": use.get("cache_read_input_tokens", 0),
                    "cache_write": use.get("cache_creation_input_tokens", 0),
                }


def logs(repo):
    """Each log of a repo with its role: the session is the writer, a sub-agent whose description names a review or a
    quiz is the reviewer."""
    home = os.environ.get("CLAUDE_CONFIG_DIR", os.path.expanduser("~/.claude"))
    folder = os.path.join(home, "projects", re.sub(r"[^A-Za-z0-9]", "-", repo))
    for path in sorted(glob.glob(f"{glob.escape(folder)}/*.jsonl")) + sorted(
            glob.glob(f"{glob.escape(folder)}/*/subagents/*.jsonl")):
        role = "writer"
        if os.path.basename(os.path.dirname(path)) == "subagents":
            meta = read_json(path[: -len(".jsonl")] + ".meta.json")
            role = "reviewer" if REVIEW.search(meta.get("description", "")) else "agent:" + meta.get("agentType", "")
        yield path, role


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


def reply(message, seen):
    """Whether a message is a model reply not yet seen: a reply is logged once per content block, with one usage."""
    if "usage" not in message or message.get("id") in seen or message.get("model") == "<synthetic>":
        return False
    seen.add(message.get("id"))
    return True


def entries(path):
    """The entries of a log. A session still running may hold a half-written last line."""
    with open(path, encoding="utf-8", errors="replace") as log:
        for line in log:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                pass


def epoch(timestamp):
    """The UTC timestamp to the second, its fraction dropped."""
    return calendar.timegm(time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S"))


def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as file:
        return json.load(file)
