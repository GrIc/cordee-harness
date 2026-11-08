---
governs: [template/cordee/bin/ledger, template/cordee/bin/harness/ledger.py, test/ledger]
---
# ledger

What agents spent on each module, by month, so that a team weighs the cost of its product's features, never of its
people. The details stay on each dev's machine, in the [cockpit](cockpit.md); the repo only keeps the sums. On by
default; with `git config cordee.ledger false`, nothing is noted, and the ledger never stops a commit or a push.

- `record` splits the tokens spent since the last commit over the modules HEAD changes, by their changed lines, into
  a note of the git notes `cordee-ledger` that hangs on a random key, written by `cordee` on the first of the month:
  [test_record_splits_a_batch_by_module_on_no_commit](/test/ledger). Each count splits whole and sums to the
  batch's: [test_record_splits_a_lone_call_without_losing_it](/test/ledger). A batch outside the modules goes to `-`:
  [test_a_batch_outside_the_modules_goes_to_a_dash](/test/ledger).
- It never notes the quiz, whatever the journal holds, since what the quiz learns about a dev stays on their machine:
  [test_record_never_notes_the_quiz](/test/ledger).
- Each window starts where the last record ended, so that an amend counts nothing twice and a failed cockpit loses
  nothing:
  [test_an_amend_counts_from_the_last_record](/test/ledger), [test_a_failed_cockpit_loses_no_window](/test/ledger).
- For a dev who turns it off, nothing is noted: [test_a_dev_who_turns_it_off_notes_nothing](/test/ledger). The hooks
  `install-hook` writes run `record` at each commit and `sync` at each push:
  [test_installed_hooks_record_and_share_the_ledger](/test/ledger).
- `sync` merges the remote's ledger into ours and pushes the result as one commit with no parent, so that two devs'
  notes add up and the shared history never shows whose came first:
  [test_sync_merges_two_devs_ledgers](/test/ledger). Two notes on one key keep both, and the next syncs go through:
  [test_sync_merges_two_notes_on_one_key](/test/ledger). A dev with no ledger fetches nothing:
  [test_sync_without_a_ledger_fetches_nothing](/test/ledger). Nor does one whose ledger a remote already took: the
  notes of others reach them with their next one, and each remote gets what it has not seen:
  [test_sync_sends_only_notes_a_remote_has_not_seen](/test/ledger).
- `report` sums the ledger by month, module, role and model, then shows per month the batches noted against the
  agent commits, marked as the hook marks them:
  [test_report_sums_by_month_module_role_and_model_then_shows_coverage](/test/ledger). Without a ledger, it says how
  to fetch it: [test_report_without_a_ledger_says_how_to_fetch_it](/test/ledger).

Constraints: as [checks](checks.md), LF line ends even on a Windows checkout:
[test_ledger_survives_a_crlf_checkout](/test/ledger). Without Python, it says nothing:
[test_without_python_only_the_commit_msg_hook_stops](/test/cockpit).
Non-goals: the readers of each agent's logs (they live in the cockpit, so a new tool changes nothing here), prices,
anonymity when one person alone worked on a module in a month (the module and the month name them), a push of every
ref (`git push --mirror`, a `refs/notes/*` refspec), which sends the local chain and its order.
