# What the review of 2026-11-02 left open

The fresh review of checks, ledger and cockpit found these; none blocks the team's test of v2.3.0. Each changes
behavior, so they come after the move to Python, which changes none, each in its own batch.

- cockpit: the hints' state is kept per worktree (`--git-path sdd/hints`) while the journal is shared, so a quiz hint
  comes back in each worktree.
- cockpit: `test/cockpit` stays off Windows in CI: Git Bash hands Python the `C:/` form of `$repo`, so the logs
  folder Python computes differs from the one the test writes to. The fix for `$PWD` below is the place to settle it.
- cockpit: `report "$PWD"` (AGENTS.md, `guide/tokens.md`) misses the logs when `$PWD` is not the real path (macOS
  `/private`, symlinks, Git Bash's `/c/...`); `git rev-parse --show-toplevel` gives it.
- ledger: a key holding different notes on two clones leaves `git notes merge` stuck, and every later sync fails while
  its NOTE says the next push retries. Keys are random, so it should never happen.
- ledger: `record` floors each module's share, so a one-call batch split over two modules notes 0 calls.
