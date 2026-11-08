---
governs: [template/cordee/bin/cockpit, template/cordee/bin/harness/cockpit.py, template/cordee/bin/harness/logs/,
  test/cockpit]
---
# cockpit

The dev's own view of where their agent tokens go, on their machine. It ships with the harness, and an upgrade
replaces it without an agent reading its diff, so that supporting a new tool costs agents nothing. The only thing it
gives away is `usage`, the sums the [ledger](ledger.md) asks for.

- `usage <repo> <since> <until>` sums the tokens spent in a repo over a window by role and exact model
  (`claude-opus-5-5`, as the tool's log names it), with output including reasoning, for each tool below, one reader
  each. Without Python, it says nothing: [test_without_python_only_the_commit_msg_hook_stops](/test/cockpit).
- Claude Code: each reply counts once, a half-written last line, a sub-agent's result and what a tool call's input
  holds are no reply; the session is the writer, a sub-agent whose description names a review or a quiz is the
  reviewer: [test_claude_code_splits_writer_and_reviewer_once_per_reply](/test/cockpit). A sub-agent revived in
  another session counts once, even after the repo or its log folder moved:
  [test_claude_code_reads_a_revived_sub_agent_once](/test/cockpit).
- opencode, a SQLite base: a child session whose title names a review is the reviewer:
  [test_opencode_child_session_is_the_reviewer](/test/cockpit).
- Kilo Code, built on opencode, reads like it from its own base, which its CLI and VS Code extension share:
  [test_kilo_code_reads_like_opencode](/test/cockpit).
- `report <repo> [<since> <until>]`, for the repo holding that folder (`$PWD` may be below its root or go through a
  symlink), over the dev's last 10 agent batches by default, shows Claude Code's cost in input-equivalent tokens (its
  provider's price ratios) by role and model, the context a session and a sub-agent start with, the longest context
  and the share of cache reads: all exact. Then, estimated from their size, what is sent along with the calls (tool
  results, skill listing, hooks, MCP instructions, memory files), each written once and read again with every later
  call: [test_report_weighs_roles_and_what_is_sent_along](/test/cockpit),
  [test_report_reads_the_last_ten_batches_by_default](/test/cockpit).
- `hints` prints what the dev's last 10 agent batches show to cut, by batch: MCP servers whose
  instructions are sent but whose tools were never called, plugins never called when the skill listing weighs 5% of
  the cost or more, anything else sent along at 5% or more, a context over 150k tokens:
  [test_hints_name_what_else_is_sent_along_and_a_long_context](/test/cockpit). The window counts batches, not days,
  so that a slow dev and a busy one get the same advice; a teammate's batch is not the dev's, who is the address git
  would write, through the mailmap and in any case:
  [test_hints_find_a_dev_with_a_plus_or_a_mailmap](/test/cockpit). Each hint comes back 10 batches later at the
  earliest, in any worktree of the clone, counted on its own branch; before the first batch or without Python, it
  says nothing:
  [test_hints_say_what_to_cut_once_in_ten_batches](/test/cockpit),
  [test_without_python_only_the_commit_msg_hook_stops](/test/cockpit).
  Over the same batches, it reads the quiz journal and names a module whose answers were flagged unclear or not what
  the dev wanted twice or more, counted once per question title and cause:
  [test_hints_name_a_module_whose_quiz_is_flagged_twice](/test/cockpit), which also shows a hint once per clone.
- A format the reader no longer reads gives no wrong figure without a word: `report` notes it and `hints` names it
  when the logs with entries in the window hold no reply it finds, or replies without a token count it knows:
  [test_report_and_hints_say_when_the_format_is_not_read](/test/cockpit).

Constraints: as [checks](checks.md); a new tool is one reader in `harness/logs/`, which `usage` finds by itself,
and `report` and `hints` too when it weighs its calls. Only that reader knows the tool's logs, names and prices.
Tested on Linux, macOS and Windows.
Non-goals: a report for opencode and Kilo Code (only their sums for now), tools whose logs we have not read yet
(Codex), telling apart two batches worked on at the same time, changing the dev's setup (the agent asks, the dev
decides).
