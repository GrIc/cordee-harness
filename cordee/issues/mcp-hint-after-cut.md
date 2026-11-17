# The MCP hint proposes a cut the dev already made

Seen on 2026-11-15, at the handoff of the batch that adds `cordee key`: `cordee hints` named claude-in-chrome, easel,
serena and four claude.ai connectors as never called, while `.claude/settings.local.json` had denied them since 16:17
the same day and the session no longer loaded them.

Why: `cockpit.hints` sums the logs of the whole window (`journal.window`), sessions from before the change included, so
a server turned off still counts until the window has moved past it. The dev reads a hint already applied and stops
trusting the others.

Leads:
- Name only the servers the latest session of the window still lists.

Where: `template/cordee/bin/harness/cockpit.py` (`hints`, `cuts`).
