# The format guard does not see a renamed attachment

Seen on 2026-11-08, when the cockpit got its format guard (decision 72): it notes logs without a reply and replies
without a token count, but not the attachments the reader looks for. If Claude Code renames `skill_listing`,
`mcp_instructions_delta` or `hook_additional_context`, `report` loses a line and a hint of `hints` never comes, without
a word.

Where: `template/cordee/bin/harness/logs/claude_code.py`, `pieces`. A lead: a log with replies in the window but no
`skill_listing` at all is suspect, since Claude Code sends one at each session start.
