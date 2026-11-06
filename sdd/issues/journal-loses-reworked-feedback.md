# The journal may lose the feedback that led to a rework

Seen on 2026-11-05 in the first field use: decision 4 of the demo repo comes from a quiz answer the dev flagged "the
code does not do what I wanted", yet `.git/sdd/quiz-journal` exists and is empty.

Guess, to check in the opencode sessions: the flag made the agent rework the batch, the reviewer wrote a new quiz for
the new batch, and the old `QUIZ.md` with its ticked box was replaced before any commit. The journal only reads the
quiz of the commit that passed, so the most useful signal, a batch redone because it was not what the dev wanted,
never reaches it.

Where: `template/sdd/bin/fabrik/journal.py`, the Quiz section of `template/sdd/WORKFLOW.md`.
