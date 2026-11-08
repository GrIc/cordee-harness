# Switch from SDD-Fabrik (for agents)

A repo with `sdd/bin/sdd` runs SDD-Fabrik, this kit's former name. Cordee is the same kit renamed: its folder,
commands, markers, refs and settings change, its rules do not. A repo deployed before SDD-Fabrik v3.3.1 first
upgrades to v3.3.1 with that tag's own `sdd/guide/upgrade.md`, which brings `sdd/config.yml` and its settings. Then
clone the new release into `<tmp>` as step 2 of the upgrade says, and:

1. Run `git mv sdd cordee`. Replace `cordee/bin/`, `cordee/guide/` and `cordee/WORKFLOW.md` with `<tmp>`'s, deleting
   `cordee/bin/sdd` and `cordee/bin/fabrik/`.
2. Replace the block between `<!-- sdd-fabrik -->` and `<!-- /sdd-fabrik -->` in `AGENTS.md` with `<tmp>`'s block
   between `<!-- cordee -->` and `<!-- /cordee -->`.
3. In the project's own files, write `cordee/` for `sdd/` and `cordee/bin/cordee` for `sdd/bin/sdd`:
   `git grep -n 'sdd/'` lists them (contracts' `governs` and links, `AGENTS.md` outside the block, `CLAUDE.md`,
   `cordee/coding-style.md`, `.gitattributes`). In `cordee/config.yml` too: a `sensitive` entry still naming `sdd/`
   matches nothing any more, and the kit's own files would stop asking a quiz without a word. Write Cordee where
   `git grep -n -i 'sdd-fabrik\|SDD audit'` finds the old name. Leave `cordee/decisions.md` as written: it is
   history.
4. CI: on GitHub, `git mv .github/workflows/sdd.yml .github/workflows/cordee.yml` and take `<tmp>`'s content; on
   GitLab, the `sdd-audit` job of `.gitlab-ci.yml` becomes `<tmp>`'s `cordee-audit`.
5. Hooks: a line that calls `sdd/bin/sdd` or `sdd/bin/ledger` now does nothing, without a word, and agent commits pass
   without their quiz. Delete the hooks that hold `# sdd-fabrik`, then run `bash cordee/bin/cordee install-hook`. A
   shared hooks folder (`git config core.hooksPath`) or a hook manager gets the lines it prints from the human, who
   keeps the old ones while other repos still run SDD-Fabrik. `bash cordee/bin/cordee doctor` then prints no NOTE
   about hooks.
6. What the harness keeps on this machine, in each clone: move `$(git rev-parse --git-common-dir)/sdd` to `cordee`
   next to it (the quiz journal, the hints shown), and in each other worktree `$(git rev-parse --git-path sdd)` to
   `$(git rev-parse --git-path cordee)` when it exists.
7. The ledger, when `refs/notes/sdd-ledger` exists: first take in what the remote holds that this clone lacks,
   `git fetch origin +refs/notes/sdd-ledger:refs/notes/sdd-ledger-remote` then
   `git notes --ref sdd-ledger merge -q -s cat_sort_uniq refs/notes/sdd-ledger-remote` (skip both when the remote has
   none). Then `git notes --ref cordee-ledger merge -q -s cat_sort_uniq refs/notes/sdd-ledger`, which keeps a note
   the new hooks already wrote, and `git update-ref -d` both old refs. The next push shares the new ref. Once every
   clone has switched, the human deletes the old one on the remote: `git push origin :refs/notes/sdd-ledger`. A clone
   or a dev with `git config sdd.ledger false` sets `git config cordee.ledger false` (`--global` when it was global).
8. Put the new source and tag on the first line of `cordee/README.md`, delete `<tmp>`, and propose a commit message
   with `Large-Batch: switches from SDD-Fabrik to Cordee`, without `Agent-Assisted` or an agent's `Co-Authored-By`: the
   files come from the kit.
