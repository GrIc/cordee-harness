# The cockpit's tests read only logs the kit wrote

Seen on 2026-11-07 in the technical premortem (risk T3): every log in `test/cockpit` is written by hand with
`reply()`, from what the kit understood of the format at the time. A reader that misreads a real version stays green.

What: one excerpt of a real Claude Code log per version the reader supports, cut down to its structure (no prompt, no
code, no path), covering the six kinds the reader uses: a reply with its usage, `skill_listing`,
`mcp_instructions_delta`, `hook_additional_context`, `instructions` or `nested_memory`, and `compact_boundary`. A new
version gets its excerpt when the reader is checked against it. It guards the kit against its own regressions, not
against a future version: the format guard does that (decision 72).
