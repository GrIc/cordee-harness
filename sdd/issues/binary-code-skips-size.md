# Code marked binary escapes the size and the coverage

Seen on 2026-11-05 by an automated security review of `c2b6b2c` (decision 48): a `.gitattributes` with `*.py binary`
or `-diff`, even in the same batch, makes `git diff --numstat` print `-` for the code, and `size.py` skips those rows.
The batch then counts no lines of code, the quiz covers no hunk, and the human reads "Binary files differ". The quiz
is still asked, since a code file changed.

Lead: a `-` row on a path a contract governs, or outside `NOT_CODE`, becomes a finding instead of being skipped. Not
`--text`: real images would count as lines.

Where: `template/sdd/bin/fabrik/size.py`, the coverage in `template/sdd/bin/fabrik/quiz.py`.
