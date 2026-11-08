---
governs: [template/sdd/bin/fabrik/quiz.py, template/sdd/bin/fabrik/journal.py]
depends: [checks]
---
# quiz

The questions that make the human understand an agent batch before it is committed. A fresh reviewer writes them, the
[checks](checks.md)' hook grades them, as the workflow's Quiz section says.

- An agent batch asks one to three questions, none when every changed file is Markdown, `.gitignore`,
  `.gitattributes` or `.gitkeep` that no contract is and no module governs (one written is still graded):
  [test_quiz_passed_adds_the_trailer_and_cleans_up](/test/run),
  [test_below_high_risk_a_quiz_asks_one_to_three_questions](/test/run),
  [test_wrong_answer_explains_then_a_retry_passes](/test/run), [test_a_markdown_only_batch_needs_no_quiz](/test/run),
  [test_markdown_and_git_files_need_no_quiz](/test/run), [test_a_governed_markdown_batch_asks_a_quiz](/test/run).
- A batch that changes or deletes a module declaring `risk: high` asks three or more, and `audit` fails until their
  `See` lines cite every hunk of code, the hook never: [test_a_high_risk_quiz_covers_every_hunk](/test/run),
  [test_a_deleted_high_risk_contract_is_high_risk](/test/run).
- A wrong answer writes its block once, in the dev's language when the key words it, and the boxes never change the
  grade: [test_a_wrong_answer_writes_a_hint_block_in_the_quiz](/test/run),
  [test_a_new_try_keeps_the_feedback_ticked](/test/run), [test_feedback_never_changes_the_grade](/test/run),
  [test_the_block_speaks_the_key_s_language](/test/run).
- Once the commit of a passed quiz exists, its flagged questions go to the journal, for all the clone's worktrees, and
  the quiz goes: [test_a_passed_quiz_journals_its_flagged_questions](/test/run),
  [test_worktrees_share_the_quiz_journal](/test/run). So a later commit-msg hook that fails keeps the quiz, a commit
  without the hook leaves none behind, and a clone whose hooks predate this clears it at the next audit or
  fingerprint, even once a merge or a pull put commits on top of the batch:
  [test_a_failing_later_hook_keeps_the_quiz](/test/run),
  [test_a_commit_without_the_hook_leaves_no_quiz](/test/run), [test_an_amend_clears_its_quiz](/test/run),
  [test_audit_clears_the_last_commit_s_quiz](/test/run),
  [test_the_next_fingerprint_clears_a_quiz_left_behind](/test/run),
  [test_a_merge_on_top_of_the_batch_still_clears_its_quiz](/test/run). A quiz left for a batch redone before any commit
  goes there once, when the next `fingerprint` runs: [test_a_reworked_batch_journals_the_old_quiz_s_flags](/test/run).
- `audit` checks its form, so that the reviewer, not the human, meets a malformed quiz:
  [test_audit_checks_the_quiz_before_the_human](/test/run), [test_a_see_line_cites_three_places_at_most](/test/run).
  It only notes a quiz older than its batch and, past one question, a right answer always in the same place:
  [test_a_quiz_older_than_the_batch_only_warns](/test/run).
- The trailer says how many hunks of code the quiz cites, outside what `not-code` lists:
  [test_the_trailer_says_how_much_the_quiz_covers](/test/run). Code that `.gitattributes` marks binary has its hunks
  too: [test_the_quiz_covers_code_marked_binary](/test/run).

Constraints: as [checks](checks.md).
