# A quiz only when intent or a boundary moves

Asked by the owner on 2026-11-05: a team, or one module, that wants no question on code. A fix or a small change within
the contract commits without a quiz; a batch that moves the module's intent or its boundaries gets questions at that
level. Set for the repo in the project file, overridden in a contract.

Why: `normal` asks code questions on every batch, `low` asks none even when intent moves, and the quiz per role in the
roadmap adds questions for other roles without taking any from the dev.

Lead: the step and its triggers are settled (decision 47), and the harness sees each trigger already: a contract's text
in the diff, `governs` and `depends` in its front matter, the modules a batch spans. `Spec-Unchanged` becomes the way
past the quiz, so the fresh reviewer checks each claim against the diff. The coverage trailer counts code hunks, which
such questions do not cite.

Where: the roadmap lines on the project config and the module's risk, `sdd/modules/checks.md`.
