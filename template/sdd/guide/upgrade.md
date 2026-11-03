# Upgrade and uninstall (for agents)

## Upgrade

1. The first line of `sdd/README.md` gives the `<source>` and the deployed tag; without a URL there, the source is
   `https://github.com/GrIc/sdd-fabrik`. `git ls-remote --tags --refs <source>` gives the latest `vX.Y.Z`.
2. `git clone <source> <tmp>`; `git -C <tmp> diff <old> <new> -- template/ ':!template/sdd/bin/'` shows what changed
   besides the scripts, which you replace without reading. Then `git -C <tmp> checkout -q <new>`.
3. Replace `sdd/WORKFLOW.md`, `sdd/guide/` and the scripts in `sdd/bin/` with the new tag's (keep the project's changes
   to `MAX_LINES`, `NOT_CODE`, `AGENT_EMAILS` and `REVIEW_WAIT_HOURS`), and the block between `<!-- sdd-fabrik -->` and
   `<!-- /sdd-fabrik -->` in `AGENTS.md`. Apply the other template changes the diff shows, such as the CI workflow, with
   the human. Put the new tag on the first line of `sdd/README.md`. Delete `<tmp>`, then run
   `bash sdd/bin/sdd install-hook`: a new version may add a hook.
4. Tell the human what changed and propose a commit message without `Agent-Assisted` or an agent's `Co-Authored-By`:
   the files come from the kit.

## Uninstall

Remove `sdd/bin/`, `sdd/guide/`, `sdd/WORKFLOW.md`, the `commit-msg`, `post-commit` and `pre-push` hooks that hold
`# sdd-fabrik` (or the `sdd/bin/` lines added to other hooks), the `sdd/bin/*` line of `.gitattributes`, the `/QUIZ.md`
line of `.git/info/exclude`, the folders `$(git rev-parse --git-common-dir)/sdd/` and, in each worktree,
`$(git rev-parse --git-path sdd)` (what the harness keeps on this machine, the quiz journal among it), the refs
`refs/notes/sdd-ledger` and `refs/notes/sdd-ledger-remote` (and on the remote, with the human), the block between the
markers in `AGENTS.md`, the `@AGENTS.md` line of `CLAUDE.md`, the `.github/workflows/sdd.yml` step, and the deny rules
added to your tool.
Ask the human before removing the project's own knowledge: `sdd/README.md`, `coding-style.md`, `modules/`,
`decisions.md` and the other topic files.
