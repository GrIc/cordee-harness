# 3.3: a quiz that asks what the module's risk calls for, and the CI on GitLab

Why: three questions on a one-line fix is too many (asked by the owner on 2026-11-05). A team, or one module, that
wants no question on code has only `low`, which asks none even when the intent moves; decision 47 settled the step
`intent` between `low` and `normal`. Some files steer the project or the harness whatever their module's risk
(`sdd/architecture.md`, the workflow, `sdd/config.yml` itself): today a Markdown one outside every module asks no
quiz, and nothing lets a module at low risk keep one file under a quiz. A batch of tests alone asks today what a batch
of code asks. Teams on GitLab replay drift and size only by hand.

## The GitLab CI file is sensitive (contracts)

- The kit's `sensitive` list holds `.gitlab-ci.yml`, as decision 58 left for this release: a batch at `low` could
  otherwise turn the CI check off with no question asked.
