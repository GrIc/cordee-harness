# Quiz answers follow predictable patterns

Seen on 2026-11-10 during review: right answers in `QUIZ.md` often follow predictable permutations because reviewer
agents avoid repeating boxes, and `audit` explicitly warns when the right answer stays in the same box across questions:
`NOTE QUIZ.md: the right answer is box B every time, vary it.` (`checks.py:31`).

Why: When answers are constrained to always differ, guessing questions 1 and 2 allows inferring question 3 by mere
elimination. Answer placement should be genuinely independent and unpredictable per question, and repeating the same box
(such as `A A A` or `C C C`) must be entirely valid.

Leads:
- Remove or adjust the warning in `checks.audit_staged` that notes identical answer ranks across questions.
- Update `WORKFLOW.md` and reviewer instructions to pick box positions independently and randomly for each question,
  without avoiding repeated letters across questions.

Where: `template/cordee/bin/harness/checks.py` (`audit_staged`), `template/cordee/WORKFLOW.md`, `test/run`.
