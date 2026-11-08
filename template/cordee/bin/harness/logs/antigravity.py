"""Antigravity CLI indexes its conversations, each with its folders and its parent, in one SQLite base, and logs each
one's steps in a transcript of its own. A sub-agent is a conversation too: the call of its parent that created it
gives its role and model."""
import datetime
import json
import os
import pathlib
import re
import sqlite3
import urllib.parse

from harness.logs import REVIEW

# The model the dev picks, as the transcript tells the agent.
PICKED = re.compile(r"setting `Model Selection` from .*? to (.+?)\. ")
CREATED = re.compile(r'"conversationId":\s*"([0-9a-f-]+)"')


def usage(repo, start, end):
    home = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity-cli")
    base = os.path.join(home, "conversation_summaries.db")
    if not os.path.exists(base):
        return
    db = sqlite3.connect(f"file:{base}?mode=ro", uri=True)
    rows = db.execute("select conversation_id, parent_conversation_id, agent_name, workspace_uris"
                      " from conversation_summaries").fetchall()
    db.close()
    folder = urllib.parse.unquote(pathlib.Path(repo).as_uri())
    ours = {cid: (parent, agent) for cid, parent, agent, uris in rows
            if folder in (urllib.parse.unquote(uri) for uri in json.loads(uris or "[]"))}
    spawned = {}
    for cid, (parent, _) in ours.items():
        if not parent:
            spawned.update(children(steps(home, cid)))
    for cid, (parent, agent) in ours.items():
        role, model = "writer", None
        if parent:
            name, model = spawned.get(cid, ("", None))
            role = "reviewer" if REVIEW.search(name) else "agent:" + agent
        for step in steps(home, cid):
            model = picked(step) or model
            # Antigravity counts tokens since October 2026: an older reply has none.
            if step.get("type") != "PLANNER_RESPONSE" or "input_tokens" not in step:
                continue
            when = datetime.datetime.fromisoformat(step["created_at"].replace("Z", "+00:00")).timestamp()
            if start < when <= end:
                yield role, model or "unknown", {
                    "input": step["input_tokens"],
                    "output": step.get("output_tokens", 0),
                    "cache_read": step.get("cache_read_tokens", 0),
                    # Antigravity logs no cache write.
                    "cache_write": 0,
                }


def steps(home, cid):
    """The steps of a conversation, from either transcript, which hold the same: a line still being written is none."""
    logs = os.path.join(home, "brain", cid, ".system_generated", "logs")
    for name in ("transcript_full.jsonl", "transcript.jsonl"):
        path = os.path.join(logs, name)
        if os.path.exists(path):
            with open(path, encoding="utf-8", errors="replace") as file:
                for line in file:
                    try:
                        yield json.loads(line)
                    except ValueError:
                        pass
            return


def picked(step):
    found = PICKED.findall(step.get("content", "")) if step.get("type") == "USER_INPUT" else []
    return found[-1] if found else None


def children(steps):
    """Each sub-agent a session created, as (its id, (role, model)): the role and model its call gave, the session's
    model when the call gave none or inherit. A call names one sub-agent or a list of them, and a reply may hold
    several calls among other tools: the steps before the next reply give their ids in the same order."""
    model, made = None, []
    for step in steps:
        model = picked(step) or model
        if step.get("type") == "PLANNER_RESPONSE":
            made = []
            for call in step.get("tool_calls") or []:
                if call.get("name") == "invoke_subagent":
                    args = {key: decoded(value) for key, value in call.get("args", {}).items()}
                    made += [(spec.get("Role", ""), spec.get("Model", "inherit"))
                             for spec in (decoded(args["Subagents"]) if "Subagents" in args else [args])]
            continue
        for cid in CREATED.findall(step.get("content", ""))[:len(made)]:
            role, given = made.pop(0)
            yield cid, (role, model if given == "inherit" else given)


def decoded(value):
    """transcript.jsonl writes each argument of a call as JSON, transcript_full.jsonl as is."""
    try:
        return json.loads(value) if isinstance(value, str) else value
    except ValueError:
        return value
