# The quiz stays home

Why: the rope team pushed each question's title, tries and causes to the shared ledger. A title names its batch, so
`git log` names who did not understand: anonymity, our first value, did not hold, and a dev who believes they are read
from above stops ticking "not understood". What the quiz learns about a dev never leaves their machine; the team gets
a fact about the code instead, in each commit: how much of the batch the quiz covered, with no aggregate. The scripts
that grew with the plan are made readable on the way. Each batch writes its decision to `docs/decisions.md` with a
`Rejected:` line (a decision it supersedes in part loses that part and points to the new one), updates the docs where
its behavior shows, and moves its criteria into its module's contract.

## Find the dev's batches as brief does (cockpit)

- `batches` takes the dev's address through the mailmap and compares it without case in awk, not as a pattern:
  `test_hints_find_a_dev_with_a_plus_or_a_mailmap`. Two lines like `brief`'s, not shared: a call across scripts
  would cost more.
- Deletes this plan and its roadmap line; then a fresh reviewer reads checks, ledger and cockpit as a whole.
