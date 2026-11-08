---
governs: [template/cordee/bin/cordee, template/cordee/bin/harness/__init__.py, template/cordee/bin/harness/__main__.py,
  template/cordee/bin/harness/git.py, template/cordee/bin/harness/drift.py,
  template/cordee/bin/harness/size.py, template/cordee/bin/harness/checks.py, template/cordee/bin/harness/hooks.py,
  template/cordee/bin/harness/doctor.py, template/cordee/bin/harness/deploy.py,
  template/.github/workflows/cordee.yml, template/.gitlab-ci.yml, test/run]
---
# checks

The script a deployed project runs at each commit and in CI: it keeps each contract in step with its code, keeps agent
batches small and asks the [quiz](quiz.md) of an agent batch. It helps, it never locks: every check can be bypassed.

- An agent batch (`Agent-Assisted: yes`, or a co-author address `agent-emails` lists) is refused on drift, on size or on
  a wrong quiz. The human's own commits only get warnings on drift and size: [test_agent_drift_blocks](/test/run),
  [test_an_agent_co_author_marks_an_agent_batch](/test/run), [test_human_drift_warns_and_commits](/test/run),
  [test_over_max_lines_blocks_an_agent_warns_a_human](/test/run). A batch whose quiz key holds its fingerprint is an
  agent batch too, whatever the message says, and the hook adds `Agent-Assisted: yes` to it:
  [test_a_quiz_written_for_the_batch_marks_an_agent_batch](/test/run). `agent-emails` in `cordee/config.yml` replaces
  the kit's addresses, and a batch that removes one is still judged by its parent's list:
  [test_the_config_lists_the_agent_emails](/test/run).
- `Bypass-Quiz: <reason>` lets an agent batch pass without a quiz, at high risk too, and the trailer stays as the
  trace; drift and size still apply. Without a reason it lifts nothing, and the hook says to write one:
  [test_bypass_quiz_with_a_reason_skips_the_quiz](/test/run), [test_bypass_quiz_holds_at_high_risk](/test/run),
  [test_bypass_quiz_still_checks_drift](/test/run), [test_bypass_quiz_still_checks_size](/test/run),
  [test_bypass_quiz_without_a_reason_asks_the_quiz](/test/run).
- A batch is judged at the highest risk, in the order `none`, `normal`, `high`, of the modules it changes, in the
  parent or in the batch; code outside every module takes the repo's. At `none` an agent batch asks no quiz and
  `cordee next` says to hand off; drift and size still apply: [test_risk_none_asks_no_quiz](/test/run). A batch that
  changes or deletes a file a `sensitive` list of the parent or of the batch matches is judged at `normal` at least:
  [test_a_sensitive_file_always_asks_a_quiz](/test/run).
- Drift: a commit that changes a module's governed paths changes its contract too, or names the module in
  `Spec-Unchanged(<module>): <reason>`, which also leaves it out of the one-module limit. A `Spec-Unchanged` naming no
  contract, or a contract with an empty `governs`, stops every commit:
  [test_spec_unchanged_spares_its_module_only](/test/run),
  [test_a_spared_module_does_not_count_toward_the_module_limit](/test/run),
  [test_errors_stop_even_a_human_commit](/test/run).
- Size: at most `batch-lines` changed lines of code and tests, and one module, unless `Large-Batch: <reason>`, which
  still notes what it lifts. `batch-lines` comes from `cordee/config.yml`, `MAX_LINES` without it. A batch that changes
  the value is judged on its own, and gets a note saying so; only its own value stops a commit when it is not a number:
  [test_the_config_sets_the_batch_lines_of_the_repo](/test/run). A contract's `batch-lines` replaces it for a batch that
  changes that module's code, higher or lower, under the same rules; SIZE names the file that sets the limit:
  [test_a_contract_sets_the_batch_lines_of_its_module](/test/run). Markdown, `.gitignore`, `.gitattributes`, `.gitkeep`
  and lock files do not count: [test_markdown_git_files_and_lockfiles_do_not_count](/test/run). `not-code` in
  `cordee/config.yml` replaces the lock files, and a batch that widens it is judged by its parent's list:
  [test_the_config_lists_what_is_not_code](/test/run). A rename counts only its edits, and prose renamed to code, or
  back, counts whole: [test_a_rename_counts_only_its_edits](/test/run). Blank lines count for nothing, added or deleted:
  [test_blank_lines_do_not_count](/test/run). A file is binary by its content, a NUL in its first 8000 bytes, never by
  `.gitattributes`: code marked `binary` or `-diff` counts, with a note that says how to read it:
  [test_code_marked_binary_still_counts](/test/run). Up to 5% over only gets a note:
  [test_over_max_lines_blocks_an_agent_warns_a_human](/test/run), [test_up_to_five_percent_over_only_notes](/test/run),
  [test_two_modules_block_an_agent](/test/run), [test_large_batch_lifts_both_limits](/test/run).
- `install-hook` writes the `commit-msg`, `post-commit` and `pre-push` hooks, or prints the line to add to a hook it did
  not write; each line passes in a repo without the harness. It says how to turn the ledger off:
  [test_install_hook_respects_an_existing_hook](/test/run),
  [test_install_hook_adds_the_ledger_hooks_that_pass_without_it](/test/run),
  [test_the_line_for_a_shared_hook](/test/run).
- `deploy <source> <tag>`, run from the kit's clone, copies into the repo the template's files it lacks, never one it
  has, with the CI file of the forge `origin` names, writes `<source> <tag>` on the first line of `cordee/README.md` and
  installs the hooks. It lists the files already there, which the agent merges, and stops, copying nothing, when the
  host of `origin` names neither GitHub nor GitLab and no `--forge` says which:
  [test_deploy_copies_what_is_missing_and_lists_the_rest](/test/run),
  [test_deploy_asks_the_forge_when_origin_names_none](/test/run).
- `touched` lists the modules a commit changes, in code or contract, each with its changed lines, so that the token
  ledger can split a batch's cost: [test_touched_lists_each_module_with_its_lines](/test/run). Before the first commit,
  it says to commit first, and `cockpit hints` says nothing:
  [test_before_the_first_commit_touched_says_so_and_the_hints_say_nothing](/test/run).
- `doctor` prints what a bug report needs: the kit's version, Python, git and the OS, the hooks folder, the ledger on
  or off, the replies each log reader found in 30 days and an audit's time. A NOTE says what to fix: a hook that does
  not run one of the kit's commands, `QUIZ.md` not kept out of git, or a `cordee/README.md` deployed from another
  version than the kit's files: [test_doctor_says_what_to_fix](/test/run). The version is raised before each tag:
  [test_the_version_is_the_last_tag_or_newer](/test/run).
- `quiet <command>` prints one line when the command passes and its last 30 lines when it fails, with its status:
  [test_quiet_hides_a_green_output_and_shows_the_end_of_a_red_one](/test/run).
- CI replays drift and size on each new commit, never the quiz: [test_range_checks_each_commit](/test/run). On
  GitLab, those of each push, and for a new branch those the default branch lacks: checked by hand on a GitLab
  project. The hook checks nothing when it finishes a merge or a cherry-pick, whose commits were checked
  when first made: [test_a_cherry_pick_asks_no_new_quiz](/test/run).
- Guidance starts with `NOTE` and never fails `audit` or a commit: the markdown ratio, which leaves out the kit's
  workflow, guides and block in `AGENTS.md` and the coding style's rows still to settle, and governs paths that match
  nothing: [test_audit_notes_the_markdown_ratio](/test/run), [test_markdown_ratio_leaves_out_the_kit_docs](/test/run),
  [test_audit_points_out_governs_paths_that_match_nothing](/test/run).

Constraints: Python 3.10, standard library only, behind a `sh` launcher, and git, on Linux, macOS and Windows (Git
Bash). `audit` of one batch takes under 3 s in a repo of 40 contracts:
[test_audit_takes_under_3_s_with_40_contracts](/test/run). Without Python, `install-hook` and the hook say what to
install, and `--no-verify` still commits: [test_without_python_only_the_commit_msg_hook_stops](/test/cockpit).
Non-goals: locks, an LLM at commit time, drift below the file level, CI for forges other than GitHub and GitLab (they
run the same command). Formats and usage: [WORKFLOW.md](../../template/cordee/WORKFLOW.md). The script's other parts:
[contracts](contracts.md), [quiz](quiz.md), [brief](brief.md).
