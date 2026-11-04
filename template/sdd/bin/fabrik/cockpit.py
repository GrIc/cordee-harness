"""The cockpit: where a dev's agent tokens go, read from the agents' own logs on this machine. Nothing leaves it but
what the token ledger asks for."""
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from types import SimpleNamespace

from fabrik import journal
from fabrik.git import agent_log, git, lines, me
from fabrik.logs import READERS
from fabrik.logs.claude_code import OUTPUT, READ, WRITE, WRITE_HOUR, logs, trace

FIELDS = ["input", "output", "cache_read", "cache_write"]
# The dev's last batches, whatever their pace: enough that "never called" means something, and a hint comes back
# after as many.
BATCHES = 10
# A hint names what costs at least this share, below which a cut does not show on the bill, or a context this long.
SHARE, LONG = 0.05, 150_000


def usage(repo, start, end):
    """For the ledger, the tokens spent in a repo between two epoch seconds: one tab-separated line per role and model
    family, with calls, input, output (reasoning included), cache read and cache write tokens."""
    rows = defaultdict(lambda: dict.fromkeys(["calls"] + FIELDS, 0))
    for reader in READERS:
        for role, model, tokens in reader.usage(repo, start, end):
            row = rows[role, family(model)]
            row["calls"] += 1
            for field in FIELDS:
                row[field] += tokens[field]
    for key in sorted(rows):
        print("\t".join(list(key) + [str(rows[key][field]) for field in ["calls"] + FIELDS]))


def family(model):
    """claude-opus-5-5 is opus: the shared ledger need not tell apart who runs which version."""
    match = re.search(r"opus|sonnet|haiku|fable", model)
    return match.group() if match else model


def report(repo, start, end):
    """Where the tokens went, for the dev to cut."""
    seen = measure(repo, start, end)
    if not seen.total:
        sys.exit(f"No Claude Code log of {repo} in that window.")
    print(f"Claude Code in {repo}: {short(seen.total)} input-equivalent tokens (cache read x{READ}, cache write"
          f" x{WRITE} or x{WRITE_HOUR}, output x{OUTPUT}).\n")
    print(f"{'role':24}{'model':10}{'calls':>7}{'tokens':>9}{'share':>7}")
    for (role, model), (calls, cost) in sorted(seen.roles.items(), key=lambda item: -item[1][1]):
        print(f"{role:24}{model:10}{calls:>7}{short(cost):>9}{cost / seen.total:>7.0%}")
    print()
    for kind, contexts in seen.starts.items():
        print(f"A {kind} starts with {short(statistics.median(contexts))} tokens of context (median of"
              f" {len(contexts)}).")
    print(f"The longest reached {short(seen.longest[0])} after {seen.longest[1]} calls; cache reads are"
          f" {seen.reads / seen.total:.0%} of the cost.\n")
    print("Estimated from their size, what is sent along with the calls:")
    for source, cost in seen.sources.most_common(8):
        print(f"{source[:40]:41}{short(cost):>9}{cost / seen.total:>7.0%}")


def measure(repo, start, end):
    """Claude Code's calls in a window: exact sums by role and model, the contexts they start with and reach, then
    estimates of what is sent along. Also each tool ever called, and the size of each plugin's skills in the listing."""
    seen = SimpleNamespace(roles=defaultdict(lambda: [0, 0]), starts=defaultdict(list), sources=Counter(),
                           called=Counter(), listing={}, total=0, reads=0, longest=(0, 0))
    for path, role in logs(repo):
        calls = 0
        for context, cost, read, model, opening in trace(path, start, end, seen):
            seen.roles[role, family(model)][0] += 1
            seen.roles[role, family(model)][1] += cost
            seen.total, seen.reads, calls = seen.total + cost, seen.reads + read, calls + 1
            seen.longest = max(seen.longest, (context, calls))
            if opening:
                seen.starts["session" if role == "writer" else "sub-agent"].append(context)
    return seen


def hints():
    """What the last batches show to cut or to write down, for the agent to put to the dev as a question. Silent before
    the first batch and when nothing is new: a hint shown comes back BATCHES batches later at the earliest."""
    repo = git("rev-parse", "--show-toplevel")
    times = batches(repo)
    if not times:
        return
    start, count = window(times)
    found = cuts(measure(repo, start, int(time.time())), count)
    for module, flags in sorted(journal.flagged(start).items()):
        if flags >= 2:
            found["quiz " + module] = (f"Quiz answers in {module} were flagged unclear or not what you wanted {flags}"
                                       f" times: propose the rule you would write.")
    state = git("rev-parse", "--git-path", "sdd/hints")
    shown = {}
    if os.path.exists(state):
        with open(state, encoding="utf-8") as file:
            shown = {key: int(batch) for key, batch in (line.rstrip("\n").split("\t") for line in file)}
    for key, text in found.items():
        if len(times) - shown.get(key, -BATCHES) >= BATCHES:
            print("HINT " + text)
            shown[key] = len(times)
    os.makedirs(os.path.dirname(state), exist_ok=True)
    with open(state, "w", encoding="utf-8", newline="") as file:
        file.writelines(f"{key}\t{batch}\n" for key, batch in shown.items())


def batches(repo):
    """The commit times of the dev's agent batches in a repo, newest first: the cockpit counts in batches, whatever the
    dev's pace. Without an address git would commit with, the dev has no batch."""
    address = me(cwd=repo)
    if address is None:
        return []
    times = []
    for line in lines(agent_log("--format=%aE%x09%ct", cwd=repo)):
        email, when = line.split("\t")
        if email.lower() == address.lower():
            times.append(int(when))
    return times


def window(times):
    """Where the last BATCHES batches start, the start of the logs when there are fewer, and how many they are."""
    return (times[BATCHES] if len(times) > BATCHES else 0), max(min(len(times), BATCHES), 1)


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


def short(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.1f}k" if n >= 1e3 else f"{n:.0f}"
