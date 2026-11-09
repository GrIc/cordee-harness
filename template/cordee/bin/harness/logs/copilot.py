"""Copilot, its CLI and VS Code's agent host, keeps a folder per session with a log of its events, one JSON a line;
a sub-agent's replies are in its session's log, under the sub-agent's id."""
import glob
import os

from harness.logs import REVIEW, entries, epoch


def usage(repo, start, end):
    home = os.environ.get("COPILOT_HOME", os.path.expanduser("~/.copilot"))
    for path in sorted(glob.glob(f"{glob.escape(home)}/session-state/*/events.jsonl")):
        events = entries(path)
        # The log opens on the session's start, which names its repo: the others are not read further.
        root = ((next(events, {}).get("data") or {}).get("context") or {}).get("gitRoot")
        if not root or not same_folder(root, repo):
            continue
        tasks = {}
        for event in events:
            if event.get("type") == "subagent.started":
                tasks[event.get("agentId")] = event["data"]
            elif event.get("type") == "session.usage_record" and start < epoch(event["timestamp"]) <= end:
                use = event["data"]["usage"]
                read, write = use.get("cacheReadTokens", 0), use.get("cacheWriteTokens", 0)
                # Gemini counts its reasoning apart from its output, Claude and GPT within: on the owner's machine,
                # 135 of Gemini's 341 replies had more reasoning than output, none of the others' 1089.
                reasoning = use.get("reasoningTokens", 0) if "gemini" in use["model"] else 0
                yield role(event, tasks), use["model"], {
                    # Copilot counts the cache in its input; the ledger, as Anthropic does, apart.
                    "input": use["inputTokens"] - read - write,
                    "output": use["outputTokens"] + reasoning,
                    "cache_read": read,
                    "cache_write": write,
                }


def same_folder(stored, repo):
    """Whether Copilot's path is the repo's: Windows writes C:\\Users\\..., git C:/Users/..., in any case."""
    return os.path.normcase(os.path.normpath(stored)) == os.path.normcase(os.path.normpath(repo))


def role(event, tasks):
    """The session is the writer, a sub-agent whose description names a review or a quiz is the reviewer."""
    if "agentId" not in event:
        return "writer"
    task = tasks.get(event["agentId"], {})
    return "reviewer" if REVIEW.search(task.get("agentDescription", "")) else "agent:" + task.get("agentName", "")
