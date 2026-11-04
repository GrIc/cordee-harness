---
governs: [template/sdd/bin/sdd, template/sdd/bin/fabrik/__init__.py, template/sdd/bin/fabrik/__main__.py,
  template/sdd/bin/fabrik/git.py, template/sdd/bin/fabrik/contracts.py, template/sdd/bin/fabrik/drift.py,
  template/sdd/bin/fabrik/size.py, template/sdd/bin/fabrik/quiz.py, template/sdd/bin/fabrik/journal.py,
  template/sdd/bin/fabrik/checks.py, template/sdd/bin/fabrik/hooks.py, template/sdd/bin/fabrik/brief.py,
  template/.github/workflows/sdd.yml, test/run]
---
# checks

The script a deployed project runs at each commit and in CI. It keeps each contract in step with its code, keeps agent
batches small, and makes the human understand an agent batch before it is committed. It helps, it never locks: every
check can be bypassed.

- An agent batch (`Agent-Assisted: yes`, or a co-author address in `AGENT_EMAILS`) is refused on drift, on size or on
  a wrong quiz. The human's own commits only get warnings on drift and size: [test_agent_drift_blocks](/test/run),
  [test_an_agent_co_author_marks_an_agent_batch](/test/run), [test_human_drift_warns_and_commits](/test/run),
  [test_over_max_lines_blocks_an_agent_warns_a_human](/test/run).
- Drift: a commit that changes a module's governed paths changes its contract too, or names the module in
  `Spec-Unchanged(<module>): <reason>`, which also leaves it out of the one-module limit. A `Spec-Unchanged` naming no
  contract, or a contract with an empty `governs`, stops every commit. `governs` entries are git pathspecs:
  [test_spec_unchanged_spares_its_module_only](/test/run),
  [test_a_spared_module_does_not_count_toward_the_module_limit](/test/run),
  [test_errors_stop_even_a_human_commit](/test/run), [test_governs_takes_git_pathspecs](/test/run).
- Size: at most `MAX_LINES` changed lines of code and tests, and one module, unless `Large-Batch: <reason>`, which
  still notes what it lifts. Up to 5% over only gets a note:
  [test_over_max_lines_blocks_an_agent_warns_a_human](/test/run), [test_up_to_five_percent_over_only_notes](/test/run),
  [test_two_modules_block_an_agent](/test/run), [test_large_batch_lifts_both_limits](/test/run).
- Quiz, on an agent batch, as the workflow's Quiz section says: three questions, none when every changed file is
  Markdown that no contract is and no module governs (one written is still graded). A batch that changes or deletes a
  module declaring `risk: high` may ask more, and `audit` fails until their `See` lines cite every hunk of code, the
  hook never: [test_quiz_passed_adds_the_trailer_and_cleans_up](/test/run),
  [test_wrong_answer_explains_then_a_retry_passes](/test/run), [test_a_high_risk_quiz_covers_every_hunk](/test/run),
  [test_a_deleted_high_risk_contract_is_high_risk](/test/run), [test_a_markdown_only_batch_needs_no_quiz](/test/run),
  [test_a_governed_markdown_batch_asks_a_quiz](/test/run). A wrong answer writes its block once, and the boxes never
  change the grade: [test_a_wrong_answer_writes_a_hint_block_in_the_quiz](/test/run),
  [test_a_new_try_keeps_the_feedback_ticked](/test/run), [test_feedback_never_changes_the_grade](/test/run), in the
  dev's language when the key words it: [test_the_block_speaks_the_key_s_language](/test/run). Once the
  commit of a passed quiz exists, its flagged questions go to the journal, for all the clone's worktrees, and the quiz
  goes: [test_a_passed_quiz_journals_its_flagged_questions](/test/run),
  [test_worktrees_share_the_quiz_journal](/test/run). So a later commit-msg hook that fails keeps the quiz, a commit
  without the hook leaves none behind, and a clone whose hooks predate this clears it at the next audit or
  fingerprint: [test_a_failing_later_hook_keeps_the_quiz](/test/run),
  [test_a_commit_without_the_hook_leaves_no_quiz](/test/run), [test_an_amend_clears_its_quiz](/test/run),
  [test_audit_clears_the_last_commit_s_quiz](/test/run),
  [test_the_next_fingerprint_clears_a_quiz_left_behind](/test/run).
  `audit` checks its form, so that the reviewer, not the human, meets a malformed quiz:
  [test_audit_checks_the_quiz_before_the_human](/test/run), [test_a_see_line_cites_three_places_at_most](/test/run).
  The trailer says how many hunks of code the quiz cites:
  [test_the_trailer_says_how_much_the_quiz_covers](/test/run).
- `install-hook` writes the `commit-msg`, `post-commit` and `pre-push` hooks, or prints the line to add to a hook it
  did not write; each line passes in a repo without the harness. It says how to turn the ledger off:
  [test_install_hook_respects_an_existing_hook](/test/run),
  [test_install_hook_adds_the_ledger_hooks_that_pass_without_it](/test/run),
  [test_the_line_for_a_shared_hook](/test/run).
- `touched` lists the modules a commit changes, in code or contract, each with its changed lines, so that the token
  ledger can split a batch's cost: [test_touched_lists_each_module_with_its_lines](/test/run).
- `brief [<module>]` prints at most three lines of what waits, without fetching: a quiz in another worktree of the
  clone, then the remote branches not merged into `origin/HEAD` (none without it) whose last commit is by another dev
  and at least `REVIEW_WAIT_HOURS` old, oldest first, with their author:
  [test_brief_shows_quizzes_waiting_in_other_worktrees](/test/run),
  [test_brief_shows_branches_waiting_for_review_with_their_author](/test/run),
  [test_brief_says_three_lines_at_most](/test/run). Given a module, it says when the dev (the author git would write)
  has no commit yet in its contract or governed paths, and names the three devs who delivered there most. It says
  nothing for a module the dev knows or not committed yet, and never reads a quiz's answers:
  [test_brief_spots_a_dev_s_first_batch_in_a_module](/test/run), [test_brief_is_silent_in_a_known_module](/test/run).
- `quiet <command>` prints one line when the command passes and its last 30 lines when it fails, with its status:
  [test_quiet_hides_a_green_output_and_shows_the_end_of_a_red_one](/test/run).
- CI replays drift and size on each new commit, never the quiz: [test_range_checks_each_commit](/test/run). The hook
  checks nothing when it finishes a merge or a cherry-pick, whose commits were checked when first made:
  [test_a_cherry_pick_asks_no_new_quiz](/test/run).
- A link in a contract, written as the workflow says, even wrapped over two lines or with an anchor, is drift when the
  commit lacks its file, or when its text is neither found as whole words in that file nor its name or path. Web links
  and links to markdown or to a directory are not checked: [test_a_link_to_a_missing_file_is_drift](/test/run),
  [test_a_link_to_a_missing_test_name_is_drift](/test/run),
  [test_audit_accepts_links_to_names_groups_and_files](/test/run), also in a worktree's hook:
  [test_a_worktree_hook_reads_relative_links](/test/run).
- Guidance starts with `NOTE` and never fails `audit` or a commit: the markdown ratio, which leaves out the kit's
  workflow and guides, governs paths that match nothing, a quiz older than its batch, a right answer always in the same
  place: [test_audit_notes_the_markdown_ratio](/test/run), [test_markdown_ratio_leaves_out_the_kit_docs](/test/run),
  [test_audit_points_out_governs_paths_that_match_nothing](/test/run),
  [test_a_quiz_older_than_the_batch_only_warns](/test/run).

Constraints: Python 3.10, standard library only, behind a `sh` launcher, and git, on Linux, macOS and Windows (Git
Bash). Without it, `install-hook` and the hook say what to install, and `--no-verify` still commits:
[test_without_python_only_the_commit_msg_hook_stops](/test/cockpit).
Non-goals: locks, an LLM at commit time, drift below the file level, CI for other forges (they run the same command).

Formats and usage: [WORKFLOW.md](../../template/sdd/WORKFLOW.md).
