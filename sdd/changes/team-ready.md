# Ready for the team

Why: the team and its management want to test the harness now. A fresh review of checks, ledger and cockpit
(2026-11-02) found what a tester would meet first: hooks that refuse where they should only advise, a quiz lost when
another hook fails, and a ledger whose history tells which clone spent what. These batches fix that on the bash
scripts, so that the human tags v2.3.0 for the team; the move to Python (decision 40) comes after it. The first batch,
committed with this plan, stops the hook's false refusals (worktree links, cherry-pick, hunk context).

## The quiz lives until its commit exists (checks)

- The hook grades and adds the trailer; the post-commit hook journals and removes `QUIZ.md` and its key once the commit
  exists, so a later commit-msg hook that fails keeps the quiz, and a commit made with `--no-verify` leaves no quiz
  behind for the next batch.

## A pushed ledger tells no clone (ledger)

- `sync` pushes the merged notes as one commit with no parent, so the shared history never shows whose notes came in
  which order. The assertions of `test/ledger` that checked nothing check again.

## The docs say what the harness does (docs)

- README (the ledger holds no quiz), `upgrade.md` (`NOT_CODE`, each worktree's folder, the ledger's refs), "nothing
  leaves the machine" worded as "nothing is pushed". Then the human tags v2.3.0.
