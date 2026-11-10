# Claude Code log reader scans entire history on every commit

Seen on 2026-11-09 during review: `claude_code.usage()` opens and parses every JSONL file in `~/.claude/projects/<slug>/`
on every commit. On a repository with 221 session logs (147 MB), `post-commit` spends over 640 ms parsing logs that hold
zero replies in the commit's window.

Why: As the project history grows, commit latency under `tokens: true` grows linearly with the lifetime session volume
instead of scaling with the active session.

Leads:
- Check `os.path.getmtime(path) < start` before opening each log file in `claude_code.py`.

Where: `template/cordee/bin/harness/logs/claude_code.py` (`usage`, `logs`).
