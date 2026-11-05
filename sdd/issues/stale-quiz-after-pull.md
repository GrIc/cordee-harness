# A quiz outlives its commit once HEAD moves on

Seen on 2026-11-04: the quiz of 12558ff (committed with `Quiz: 3/3`) was still in `QUIZ.md` after the merge of
`python-harness` and the pull on main, and `audit` graded it against the next batch ("needs a See line").

Why: the clone runs a shared hooks folder (`core.hooksPath=~/.git-hooks`) whose `post-commit` predates the line that
calls `committed`. The fallback in the next audit, commit or fingerprint only matches the quiz against `HEAD^` and
`HEAD@{1}` (`template/sdd/bin/fabrik/journal.py:25`); after a pull HEAD is a merge commit, so it never matches and the
quiz stays, its flagged questions never reach the journal.

Where: `journal.committed`. A lead: look for the fingerprint among the commits reachable from HEAD that carry a
`Quiz:` trailer, or tell the dev the hooks are out of date.
