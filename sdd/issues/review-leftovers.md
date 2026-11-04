# What the review of 2026-11-02 left open

The fresh review of checks, ledger and cockpit found these; none blocks the team's test of v2.3.0. Each changes
behavior, so they come after the move to Python, which changes none, each in its own batch.

- cockpit: four criteria no test pins (anything else sent along at 5% or more, a context over 150k tokens, `report`'s
  default window of 10 batches, the dev's own address through the mailmap in `batches`): each mutation leaves
  `test/cockpit` green.
- cockpit: the hints' state is kept per worktree (`--git-path sdd/hints`) while the journal is shared, so a quiz hint
  comes back in each worktree.
- cockpit: `test/cockpit` stays off Windows in CI: Git Bash hands Python the `C:/` form of `$repo`, so the logs
  folder Python computes differs from the one the test writes to. The fix for `$PWD` below is the place to settle it.
- cockpit: `report "$PWD"` (AGENTS.md, `guide/tokens.md`) misses the logs when `$PWD` is not the real path (macOS
  `/private`, symlinks, Git Bash's `/c/...`); `git rev-parse --show-toplevel` gives it.
- checks: `governs` written as a YAML scalar or block list spills into the next keys (`risk`, `high` become paths).
- ledger: a key holding different notes on two clones leaves `git notes merge` stuck, and every later sync fails while
  its NOTE says the next push retries. Keys are random, so it should never happen.
- ledger: `record` floors each module's share, so a one-call batch split over two modules notes 0 calls.
- checks: `checks.md` is over the 50-line rule; moving the quiz into its own module would bring both under it.
- checks: a `governs` entry outside the repo (`../shared/`) stops every audit and commit with git's bare `fatal`, and
  `cockpit hints` or `sdd touched` in a repo with no commit exit 128. The bash version printed the same `fatal`, then
  went on and missed the drift; the error should name the contract and what to do.
