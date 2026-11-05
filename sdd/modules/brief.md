---
governs: [template/sdd/bin/fabrik/brief.py]
depends: [checks]
---
# brief

What waits for the dev, read before a batch so that they finish it before producing more.

- `brief [<module>]` prints at most three lines of what waits, without fetching: a quiz in another worktree of the
  clone, then the remote branches not merged into `origin/HEAD` (none without it) whose last commit is by another dev
  and at least `REVIEW_WAIT_HOURS` old, oldest first, with their author:
  [test_brief_shows_quizzes_waiting_in_other_worktrees](/test/run),
  [test_brief_shows_branches_waiting_for_review_with_their_author](/test/run),
  [test_brief_says_three_lines_at_most](/test/run). Given a module, it says when the dev (the author git would write)
  has no commit yet in its contract or governed paths, and names the three devs who delivered there most. It says
  nothing for a module the dev knows or not committed yet, and never reads a quiz's answers:
  [test_brief_spots_a_dev_s_first_batch_in_a_module](/test/run), [test_brief_is_silent_in_a_known_module](/test/run).

Constraints: as [checks](checks.md).
