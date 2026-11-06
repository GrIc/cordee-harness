# 3.3: a quiz that asks what the module's risk calls for, and the CI on GitLab

Why: three questions on a one-line fix is too many (asked by the owner on 2026-11-05). A team, or one module, that
wants no question on code has only `low`, which asks none even when the intent moves; decision 47 settled the step
`intent` between `low` and `normal`. Some files steer the project or the harness whatever their module's risk
(`sdd/architecture.md`, the workflow, `sdd/config.yml` itself): today a Markdown one outside every module asks no
quiz, and nothing lets a module at low risk keep one file under a quiz. A batch of tests alone asks today what a batch
of code asks. Teams on GitLab replay drift and size only by hand.

## The CI on GitLab (checks)

- `template/.gitlab-ci.yml`, governed by checks, replays drift and size on each new commit of a merge request
  (from `CI_MERGE_REQUEST_DIFF_BASE_SHA`) or of a push to a branch without an open merge request (from
  `CI_COMMIT_BEFORE_SHA`), with the full history; a new branch, whose base is zeros, audits its tip. Checked by hand
  on a GitLab project.
- The deploy copies the CI file of the repo's forge, read from its remote or asked of the human, merges its job into
  an existing `.gitlab-ci.yml`, and the README, the upgrade guide and the uninstall name it.
- The contract drops "CI for other forges" from its non-goals; a decision says why.
