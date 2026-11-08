# Upgrade and uninstall (for agents)

## Upgrade

1. The first line of `cordee/README.md` gives the `<source>` and the deployed tag; without a URL there, the source is
   `https://github.com/GrIc/cordee-harness`. `git ls-remote --tags --refs <source>` gives the latest `vX.Y.Z`.
2. `git clone <source> <tmp>`; `git -C <tmp> diff <old> <new> -- template/ ':!template/cordee/bin/'` shows what changed
   besides the scripts, which you replace without reading. Then `git -C <tmp> checkout -q <new>`. A repo with
   `sdd/bin/sdd` instead of `cordee/bin/cordee` follows [from-sdd-fabrik.md](from-sdd-fabrik.md) from here.
3. Coming from a version before 3.0.0, whose scripts were all shell, check first that the human has Python 3.10 or later
   (`python3 --version`, or `python`, or `py -3`); if not, tell them how to install it for their system, and stop.
   Replace `cordee/WORKFLOW.md`, `cordee/guide/` and `cordee/bin/` with the new tag's, deleting what it no longer has,
   such as `cordee/bin/cockpit.py`. `cordee/config.yml` is the project's and stays; coming from a version without it,
   copy the new tag's. Write a project's change to `MAX_LINES` in it as `batch-lines`, to `REVIEW_WAIT_HOURS` as
   `review-wait-hours`, to `AGENT_EMAILS` as `agent-emails` and to `NOT_CODE` as `not-code`, a list each, and append the
   new tag's commented settings that the project's file lacks. Replace the block between `<!-- cordee -->` and `<!--
   /cordee -->` in `AGENTS.md`. Apply the other template changes the diff shows with the human. A CI change goes only to
   the repo's forge: `.github/workflows/cordee.yml` on GitHub, the `cordee-audit` job of `.gitlab-ci.yml` on GitLab. A
   GitLab repo without that job gets it as the deploy adds it, and loses `.github/workflows/cordee.yml`, which GitLab
   never runs. Put the new tag on the first line of `cordee/README.md`. Delete `<tmp>`, then run `bash cordee/bin/cordee
   install-hook`: a new version may add a hook.
4. Tell the human what changed and propose a commit message without `Agent-Assisted` or an agent's `Co-Authored-By`:
   the files come from the kit.

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
