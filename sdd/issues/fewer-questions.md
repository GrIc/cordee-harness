# One question for a batch of one hunk

Asked by the owner on 2026-11-05: three questions on a one-line fix is too many.

Lead: one to three questions at normal risk, fewer than three only when their `See` lines cite every hunk of code,
which `cover` already counts (`template/sdd/bin/fabrik/quiz.py:114`). High risk keeps three or more. The count is
fixed today at `template/sdd/bin/fabrik/quiz.py:45-48`. It carries decision 39 further: the reach sets the quiz, not a
count.

A batch with no hunk of code, such as a contract alone, asks one question.

Where: `quiz.form`, the Quiz section of `template/sdd/WORKFLOW.md`, `sdd/modules/checks.md`.
