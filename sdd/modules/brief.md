---
governs: [template/sdd/bin/fabrik/brief.py]
depends: [checks]
---
# brief

What waits for the dev, read before a batch so that they finish it before producing more, and the step left in a
batch, read from git rather than remembered.

- `brief [<module>]` prints at most three lines of what waits, without fetching: a quiz in another worktree of the
  clone, then the remote branches not merged into `origin/HEAD` (none without it) whose last commit is by another dev,
  not a bot, at least `review-wait-hours` old (4) and less than `abandoned-days` (14), oldest first, with their author:
  [test_brief_shows_quizzes_waiting_in_other_worktrees](/test/run),
  [test_brief_shows_branches_waiting_for_review_with_their_author](/test/run),
  [test_brief_says_three_lines_at_most](/test/run). Both settings come from `sdd/config.yml` at HEAD, and a value that
  is not a whole number stops `brief` with an ERROR that says what to write:
  [test_the_config_sets_how_long_a_branch_waits](/test/run). Given a module, it says when the dev (the author git would
  write) has no commit yet in its contract or governed paths, and names the three devs who delivered there most. It says
  nothing for a module the dev knows or not committed yet, and never reads a quiz's answers:
  [test_brief_spots_a_dev_s_first_batch_in_a_module](/test/run), [test_brief_is_silent_in_a_known_module](/test/run).
- `next` prints the one step of COMPILE left, from the state of the batch in git, and always exits 0: nothing to
  propose when no tracked file changed; step 5 while tracked files are changed and not staged, or the message is
  missing or older than the last commit; the audit's findings, drift as step 3 and the others as step 5; step 6 while a
  batch that asks a quiz, without `Bypass-Quiz`, has a quiz missing, malformed or older than the batch; else step 7, the
  handoff. It lists the untracked files, which never block: [test_next_leads_a_batch_to_its_quiz](/test/run),
  [test_next_sends_size_to_step_5_and_skips_a_quiz_not_asked](/test/run).

Constraints: as [checks](checks.md).
