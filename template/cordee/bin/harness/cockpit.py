"""The cockpit: where a dev's agent tokens go, read from the agents' own logs on this machine. Nothing leaves it but
what the token ledger asks for."""
import statistics
import sys
import time
from collections import defaultdict
from types import SimpleNamespace

from harness import journal
from harness.git import git
from harness.logs import MCP, READERS, SKILLS, Sent, label

FIELDS = ["input", "output", "cache_read", "cache_write"]
# A hint names what costs at least this share, below which a cut does not show on the bill, or a context this long.
SHARE, LONG = 0.05, 150_000


def usage(repo, start, end):
    """For the ledger, the tokens spent in a repo between two epoch seconds: one tab-separated line per role and exact
    model, with calls, input, output (reasoning included), cache read and cache write tokens."""
    rows = defaultdict(lambda: dict.fromkeys(["calls"] + FIELDS, 0))
    for reader in READERS:
        for role, model, tokens in reader.usage(repo, start, end):
            row = rows[role, model]
            row["calls"] += 1
            for field in FIELDS:
                row[field] += tokens[field]
    for key in sorted(rows):
        print("\t".join(list(key) + [str(rows[key][field]) for field in ["calls"] + FIELDS]))


def report(repo, start=None, end=None):
    """Where the tokens went, for the dev to cut: a part per tool that can weigh its calls. By default, over the dev's
    last journal.BATCHES batches."""
    # The agents name their logs from the repo's real path, which $PWD may not be: a symlink, macOS's /private, a
    # folder below the root.
    repo = git("-C", repo, "rev-parse", "--show-toplevel")
    if start is None:
        start, end = journal.window(journal.batches(repo))[0], int(time.time())
    measured = measures(repo, start, end)
    for seen in measured:
        for text in unread(seen).values():
            print("NOTE " + text)
    weighed = [seen for seen in measured if seen.total]
    if not weighed:
        sys.exit(f"No agent log of {repo} that the cockpit can weigh in that window.")
    for seen in weighed:
        show(repo, seen)


def show(repo, seen):
    print(f"{seen.reader.NAME} in {repo}: {short(seen.total)} input-equivalent tokens ({seen.reader.PRICES}).\n")
    print(f"{'role':24}{'model':26}{'calls':>7}{'tokens':>9}{'share':>7}")
    for (role, model), (calls, cost) in sorted(seen.roles.items(), key=lambda item: -item[1][1]):
        print(f"{role:24}{model:26}{calls:>7}{short(cost):>9}{cost / seen.total:>7.0%}")
    print()
    for kind, contexts in seen.starts.items():
        print(f"A {kind} starts with {short(statistics.median(contexts))} tokens of context (median of"
              f" {len(contexts)}).")
    print(f"The longest reached {short(seen.longest[0])} after {seen.longest[1]} calls; cache reads are"
          f" {seen.reads / seen.total:.0%} of the cost.\n")
    print("Estimated from their size, what is sent along with the calls:")
    for source, cost in seen.sent.costs.most_common(8):
        print(f"{label(source)[:40]:41}{short(cost):>9}{cost / seen.total:>7.0%}")


def measures(repo, start, end):
    """What each tool that can weigh its calls shows in a window."""
    return [measure(reader, repo, start, end) for reader in READERS if hasattr(reader, "calls")]


def measure(reader, repo, start, end):
    """A tool's calls in a window: exact sums by role and model, the contexts they start with and reach, then
    estimates of what is sent along."""
    seen = SimpleNamespace(reader=reader, roles=defaultdict(lambda: [0, 0]), starts=defaultdict(list), sent=Sent(),
                           total=0, reads=0, longest=(0, 0))
    for call in reader.calls(repo, start, end, seen.sent):
        seen.roles[call.role, call.model][0] += 1
        seen.roles[call.role, call.model][1] += call.cost
        seen.total, seen.reads = seen.total + call.cost, seen.reads + call.read
        seen.longest = max(seen.longest, (call.context, call.rank))
        if call.opens:
            seen.starts["session" if call.role == "writer" else "sub-agent"].append(call.context)
    return seen


def hints():
    """What the last batches show to cut, for the agent to put to the dev as a question; journal.show says when."""
    repo = git("rev-parse", "--show-toplevel")
    times = journal.batches(repo)
    if not times:
        return
    start, count = journal.window(times)
    found = {}
    for seen in measures(repo, start, int(time.time())):
        found.update(unread(seen))
        found.update(cuts(seen, count))
    journal.show(found, times)


def unread(seen):
    """What tells a format the reader no longer reads, whose figures are then wrong without a word: logs with entries in
    the window but no reply it finds, or replies without a token count it knows."""
    found, name = {}, seen.reader.NAME
    tell = "its format may have changed: send bash cordee/bin/cordee doctor's output in a bug report to the kit."
    if seen.sent.logs and not seen.roles:
        found["format " + name] = f"{name}'s logs with entries in this window hold no reply the cockpit reads: {tell}"
    if seen.sent.blank:
        found["tokens " + name] = (f"{seen.sent.blank} of {name}'s replies in this window hold no token count the"
                                   f" cockpit reads, so its figures are too low: {tell}")
    return found


def cuts(seen, count):
    """What a tool's calls show to cut, by kind."""
    found, sent = {}, seen.sent
    if not seen.total:
        return found
    servers = {name: cost for (kind, name), cost in sent.costs.items() if kind == MCP}
    unused = sorted(set(servers) - sent.servers_called)
    if unused:
        found["mcp"] = (f"MCP servers never called in this repo's logs, whose instructions cost"
                        f" {short(sum(servers[server] for server in unused) / count)} tokens a batch:"
                        f" {', '.join(unused)}.")
    listing = sent.costs[SKILLS, ""]
    idle = {plugin: size for plugin, size in sent.plugin_sizes.items() if plugin not in sent.plugins_called}
    if listing >= SHARE * seen.total and idle:
        found["skills"] = (f"The skill listing costs {short(listing / count)} tokens a batch"
                           f" ({listing / seen.total:.0%}); plugins whose skills were never called here make"
                           f" {sum(idle.values()) / sum(sent.plugin_sizes.values()):.0%} of it, the largest:"
                           f" {', '.join(sorted(idle, key=idle.get, reverse=True)[:5])}.")
    for source, cost in sent.costs.items():
        if cost >= SHARE * seen.total and source[0] not in (MCP, SKILLS):
            text = label(source)
            found[text] = (f"{text[0].upper()}{text[1:]} cost {short(cost / count)} tokens a batch"
                           f" ({cost / seen.total:.0%}), sent again with every later call.")
    if seen.longest[0] > LONG:
        found["context"] = (f"A log reached {short(seen.longest[0])} tokens of context, read again with each call: a"
                            f" fresh session per batch reads less.")
    return found


def short(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.1f}k" if n >= 1e3 else f"{n:.0f}"
