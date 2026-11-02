# The quiz stays home

Why: the rope team pushed each question's title, tries and causes to the shared ledger. A title names its batch, so
`git log` names who did not understand: anonymity, our first value, did not hold, and a dev who believes they are read
from above stops ticking "not understood". What the quiz learns about a dev never leaves their machine; the team gets
a fact about the code instead, in each commit: how much of the batch the quiz covered, with no aggregate. The scripts
that grew with the plan are made readable on the way. Each batch writes its decision to `docs/decisions.md` with a
`Rejected:` line (a decision it supersedes in part loses that part and points to the new one), updates the docs where
its behavior shows, and moves its criteria into its module's contract.

## The quiz covers the batch (checks)

- A `See` line cites one to three places, `file:line` or `file:line-line`, separated by `, `. A hunk of
  `git diff -U0` outside Markdown and lock files (the size count's filter, shared; tests count) is covered when a
  cited range meets its new-side lines, or for a hunk that only deletes, its new-side line or the next one (`file:1`
  for a deleted file). A new file is one hunk. The hook writes `Quiz: 3/3, covers 5/7`, or `Quiz: 3/3` with no code
  hunk: `test_the_trailer_says_how_much_the_quiz_covers`, `test_a_see_line_cites_three_places_at_most`.
- At high risk the quiz has three questions or more and `audit` fails until every hunk is covered; its note says so
  instead of "five". The hook never checks coverage, so the human is never refused for it:
  `test_a_high_risk_quiz_covers_every_hunk`, in place of `test_a_high_risk_module_asks_five_questions`. Otherwise,
  three questions.
- WORKFLOW: questions ask what this code does, never the technology, from what it does to how, then why. Decision 39
  supersedes the five questions of 31 and says that a new file is one hunk.

## Find the dev's batches as brief does (cockpit)

- `batches` takes the dev's address through the mailmap and compares it without case in awk, not as a pattern:
  `test_hints_find_a_dev_with_a_plus_or_a_mailmap`. Two lines like `brief`'s, not shared: a call across scripts
  would cost more.
- Deletes this plan and its roadmap line; then a fresh reviewer reads checks, ledger and cockpit as a whole.
