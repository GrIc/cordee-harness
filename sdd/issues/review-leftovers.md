# What the review of 2026-11-02 left open

The fresh review of checks, ledger and cockpit found these; none blocks the team's test of v2.3.0. Each changes
behavior, so they come after the move to Python, which changes none, each in its own batch.

- checks: `governs` written as a YAML scalar or block list spills into the next keys (`risk`, `high` become paths).
- checks: `checks.md` is over the 50-line rule; moving the quiz into its own module would bring both under it.
- checks: a `governs` entry outside the repo (`../shared/`) stops every audit and commit with git's bare `fatal`, and
  `cockpit hints` or `sdd touched` in a repo with no commit exit 128. The bash version printed the same `fatal`, then
  went on and missed the drift; the error should name the contract and what to do.
