# A flag is lost when the quiz is rewritten for the same batch

Seen on 2026-11-08, in the review of the batch that journals a reworked quiz (decision 69): the dev ticks "the
question is unclear" on a batch that stays as it was, and the agent has the quiz rewritten for that same batch.
`fingerprint` sees a key that matches the staged batch, journals nothing, and the new `QUIZ.md` replaces the old one.
An "unclear" flag is the one that should improve the questions, and it is the one that goes.

Where: `journal.reworked` (`template/cordee/bin/harness/journal.py`), which tells a replaced quiz only by its
fingerprint.
