# Upgrade and uninstall (for agents)

## Upgrade

1. The first line of `cordee/README.md` gives `<source>` and the deployed tag `<old>`; without a URL there, `<source>`
   is `https://github.com/GrIc/cordee-harness`. `git ls-remote --tags --refs <source>` gives the latest `vX.Y.Z`
   (`<new>`).
2. `git clone --branch <new> <source> <tmp>`. A repo with `sdd/bin/sdd` instead of `cordee/bin/cordee` follows
   [from-sdd-fabrik.md](from-sdd-fabrik.md) from here.
3. Run `bash <tmp>/template/cordee/bin/cordee deploy <source> <new>` (with `--forge github` or `--forge gitlab` when it
   asks). It replaces `cordee/bin/`, `cordee/guide/`, `cordee/WORKFLOW.md`, the Cordee block in `AGENTS.md` and the
   first line of `cordee/README.md`, copies any new file of `template/` the repo lacks, and updates the hooks (when a
   hook is already in place, show the human the lines it printed).
4. `git -C <tmp> diff <old> <new> -- template/ ':!template/cordee/bin/' ':!template/cordee/guide/'
   ':!template/cordee/WORKFLOW.md' ':!template/AGENTS.md'` shows what changed in the files `deploy` left as they were.
   Append to `cordee/config.yml` the new commented settings it lacks; apply a CI change only to the repo's forge
   (`.github/workflows/cordee.yml` on GitHub, the `cordee-audit` job of `.gitlab-ci.yml` on GitLab); apply the rest with
   the human.
5. Delete `<tmp>`, tell the human what changed, and propose a commit message without `Agent-Assisted` or an agent's
   `Co-Authored-By`: the files come from the kit.

## Uninstall

Remove `cordee/bin/`, `cordee/guide/`, `cordee/WORKFLOW.md`, `cordee/config.yml`, the `commit-msg`, `post-commit` and
`pre-push` hooks that hold `# cordee` (or the `cordee/bin/` lines added to other hooks), the `cordee/bin/*` line of
`.gitattributes`, the `/QUIZ.md` line of `.git/info/exclude`, the folders `$(git rev-parse --git-common-dir)/cordee/`
and, in each worktree, `$(git rev-parse --git-path cordee)` (what the harness keeps on this machine, the quiz journal
among it), the refs `refs/notes/cordee-ledger` and `refs/notes/cordee-ledger-remote` (and on the remote, with the
human), the block between the markers in `AGENTS.md`, the `@AGENTS.md` line of `CLAUDE.md`, the
`.github/workflows/cordee.yml` step or the `cordee-audit` job of `.gitlab-ci.yml`, and the deny rules added to your
tool. Ask the human before removing the project's own knowledge: `cordee/README.md`, `coding-style.md`, `modules/`,
`decisions.md` and the other topic files.
