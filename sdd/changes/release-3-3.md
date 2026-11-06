# 3.3: a quiz that asks what the module's risk calls for, and the CI on GitLab

Why: three questions on a one-line fix is too many (asked by the owner on 2026-11-05). A team, or one module, that
wants no question on code has only `low`, which asks none even when the intent moves; decision 47 settled the step
`intent` between `low` and `normal`. Some files steer the project or the harness whatever their module's risk
(`sdd/architecture.md`, the workflow, `sdd/config.yml` itself): today a Markdown one outside every module asks no
quiz, and nothing lets a module at low risk keep one file under a quiz. A batch of tests alone asks today what a batch
of code asks. Teams on GitLab replay drift and size only by hand.

## A sensitive file always asks a quiz (contracts and checks, Large-Batch)

The setting and its only reader land together, since the tests reach the script through its commands alone; the
human adds `Large-Batch: the sensitive setting and its check`. About 200 lines with the tests.

- `sensitive` lists one entry per `- ` line below the key, or one entry on the key's line, in a contract's front
  matter or in `sdd/config.yml`; an entry is never split, a comment starts at ` #`, quotes around it go, and one that
  starts with `[`, other than `[]`, stops the commit with an ERROR that shows the `- ` form. A file matches its own
  path from the repo root, a folder (ending with `/`, never starting with one) every path under it, a regular
  expression between slashes, with at least one character, every path it is found in.
- Unset in `sdd/config.yml`, the list is the kit's: `sdd/bin/`, `sdd/WORKFLOW.md`, `sdd/guide/`, `sdd/config.yml`,
  `AGENTS.md`, `CLAUDE.md`, `sdd/architecture.md`, `sdd/coding-style.md`, `sdd/product.md`, `sdd/modules/`. Set, it
  replaces it, and `sensitive: []` lists none. A contract's list adds to the repo's, for any file of the batch.
- A batch that changes or deletes a file that the list of the base or of the tree matches is judged at normal risk at
  least: at low or intent it asks a quiz of one to three questions, at high it keeps high's rules. The trailer is the
  usual one.
- A regular expression that does not compile stops the commit with an ERROR that quotes it; in the base, it is left
  out.
- The commented `sensitive` line of `sdd/config.yml`, the Contracts and Quiz sections of the workflow say so, and a
  decision supersedes 48 for the files the list matches.

## A batch of tests alone asks one step less (checks)

- A batch whose changed files are all files a contract links to, other than Markdown and folders, along with
  Markdown and git's own files that no module governs and no `sensitive` list matches, is judged one step lower: high
  gives normal, normal gives intent, intent gives low.
- The list of linked files comes out of `contracts.links`, a refactor that keeps its findings, under
  `Spec-Unchanged(contracts)`.
- The Quiz section of the workflow says so, and a decision says why, and what was rejected.

## The CI on GitLab (checks)

- `template/.gitlab-ci.yml`, governed by checks, replays drift and size on each new commit of a merge request
  (from `CI_MERGE_REQUEST_DIFF_BASE_SHA`) or of a push to a branch without an open merge request (from
  `CI_COMMIT_BEFORE_SHA`), with the full history; a new branch, whose base is zeros, audits its tip. Checked by hand
  on a GitLab project.
- The deploy copies the CI file of the repo's forge, read from its remote or asked of the human, merges its job into
  an existing `.gitlab-ci.yml`, and the README, the upgrade guide and the uninstall name it.
- The contract drops "CI for other forges" from its non-goals; a decision says why.
