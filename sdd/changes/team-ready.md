# Ready for the team

Why: the team and its management want to test the harness now. A fresh review of checks, ledger and cockpit
(2026-11-02) found what a tester would meet first: hooks that refuse where they should only advise, a quiz lost when
another hook fails, and a ledger whose history tells which clone spent what. These batches fix that on the bash
scripts, so that the human tags v2.3.0 for the team; the move to Python (decision 40) comes after it. The first batch,
committed with this plan, stops the hook's false refusals (worktree links, cherry-pick, hunk context).

## Audit clears the last commit's quiz, the docs say what the harness does (checks)

- `audit` runs `committed` first, as the hook and `fingerprint` do, so that a quiz left by a clone whose hooks predate
  the post-commit line is not graded as the staged batch's.

- README (the ledger holds no quiz), `upgrade.md` (`NOT_CODE`, each worktree's folder, the ledger's refs), "nothing
  leaves the machine" worded as "nothing is pushed". Then the human tags v2.3.0.
