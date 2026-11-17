"""Codex keeps a log per thread, one JSON a line, under sessions/<year>/<month>/<day>/. It opens on the thread's
session_meta, which names its folder; a sub-agent is a thread of its own."""
import glob
import os
from collections import Counter

from harness.logs import REVIEW, SKILLS, Call, Sent, entries, epoch

# OpenAI's price ratios for GPT-5, in input tokens: a cached input token costs a tenth, an output token 8.
READ, OUTPUT = 0.1, 8
# The token counts of a reply's usage.
TOKENS = {"input_tokens", "cached_input_tokens", "output_tokens"}
# Text runs about 4 characters a token.
CHARS_PER_TOKEN = 4

NAME = "Codex"
PRICES = f"cached input x{READ}, output x{OUTPUT}"


def usage(repo, start, end):
    for path, role in logs(repo, start):
        for model, use, _ in trace(path, start, end, Sent()):
            read, write = use.get("cached_input_tokens", 0), use.get("cache_write_input_tokens", 0)
            yield role, model, {
                # Codex counts the cache in its input; the ledger, as Anthropic does, apart.
                "input": use.get("input_tokens", 0) - read - write,
                # Reasoning is within the output: input and output sum to the reply's total.
                "output": use.get("output_tokens", 0),
                "cache_read": read,
                "cache_write": write,
            }


def calls(repo, start, end, sent):
    for path, role in logs(repo, start):
        for rank, (model, use, opens) in enumerate(trace(path, start, end, sent), 1):
            read = READ * use.get("cached_input_tokens", 0)
            cost = (use.get("input_tokens", 0) - use.get("cached_input_tokens", 0) + read
                    + OUTPUT * use.get("output_tokens", 0))
            yield Call(role, model, use.get("input_tokens", 0), cost, read, opens, rank)


def logs(repo, start):
    """Each log of a repo written to since start, with its role: a thread the dev opened is the writer, a sub-agent
    whose path or role names a review or a quiz is the reviewer."""
    home = os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))
    for path in sorted(glob.glob(f"{glob.escape(home)}/sessions/*/*/*/*.jsonl")):
        if os.path.getmtime(path) < start:
            continue
        first = next(entries(path), {})
        thread = (first.get("payload") or {}) if first.get("type") == "session_meta" else {}
        if not below(thread.get("cwd") or "", repo):
            continue
        role = "writer"
        if thread.get("thread_source") == "subagent":
            name = f"{thread.get('agent_path') or ''} {thread.get('agent_role') or ''}"
            role = "reviewer" if REVIEW.search(name) else "agent:" + (thread.get("agent_role") or "")
        yield path, role


def below(folder, repo):
    """Whether Codex ran in the repo or in a folder of it, whatever the slashes and the case of a Windows path."""
    folder, repo = (os.path.normcase(os.path.normpath(path)) for path in (folder, repo))
    return folder == repo or folder.startswith(repo + os.sep)


def trace(path, start, end, sent):
    """Each reply of a log in the window, as its model, its usage and whether it is the log's first. Adds to
    sent.costs what each piece sent along costs: sent once at the input price, then read again from the cache with
    every later call until a compaction drops it."""
    live, pending, names, model, total, replies, active = Counter(), Counter(), {}, "", None, 0, False
    for entry in entries(path):
        kind, payload = entry.get("type"), entry.get("payload") or {}
        if not active and "timestamp" in entry and start < epoch(entry["timestamp"]) <= end:
            active = True
            sent.logs += 1
        if kind == "turn_context":
            model = payload.get("model", model)
        elif kind == "compacted":
            live.clear()
        elif kind == "world_state":
            state = payload.get("state") or {}
            pending["memory files (AGENTS.md)", ""] += tokens((state.get("agents_md") or {}).get("text"))
            pending[SKILLS, ""] += tokens((state.get("host_skills") or {}).get("body"))
        elif kind == "response_item" and payload.get("type") in ("function_call", "custom_tool_call"):
            names[payload.get("call_id")] = payload.get("namespace") or payload.get("name") or "?"
        elif kind == "response_item" and payload.get("type") in ("function_call_output", "custom_tool_call_output"):
            pending["tool results", names.get(payload.get("call_id"), "?")] += tokens(payload.get("output"))
        elif kind == "event_msg" and payload.get("type") == "token_count" and payload.get("info"):
            # A count said again, as with a new rate limit, is no new reply.
            if payload["info"].get("total_token_usage") == total:
                continue
            total, use = payload["info"].get("total_token_usage"), payload["info"].get("last_token_usage") or {}
            replies += 1
            if start < epoch(entry["timestamp"]) <= end:
                if not TOKENS.intersection(use):
                    sent.blank += 1
                for source, size in live.items():
                    sent.costs[source] += READ * size
                sent.costs.update(pending)
                yield model, use, replies == 1
            live.update(pending)
            pending.clear()


def tokens(content):
    return len(content if isinstance(content, str) else str(content or "")) / CHARS_PER_TOKEN
