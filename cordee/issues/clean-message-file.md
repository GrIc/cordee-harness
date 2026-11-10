# The proposed commit message file persists after commit

Seen on 2026-11-09 during code review: `.git/cordee/message` is created at step 5 of `COMPILE`, but `journal.committed()`
only deletes `QUIZ.md` and `cordee/quiz-key`.

Why: `brief.step_left` uses `os.path.getmtime(path) < int(last_commit)` to judge whether the message is stale. If a commit
occurs in the same second as the file write (common with `risk: none` or `Bypass-Quiz`), or if a developer resets with
`git reset --soft HEAD^`, `last_commit` can be equal to or older than the file's mtime, letting a previous batch's message
linger and be accepted for the next batch.

Leads:
- Remove `.git/cordee/message` inside `journal.committed()` as soon as the commit is verified.

Where: `template/cordee/bin/harness/journal.py` (`committed`), `template/cordee/bin/harness/brief.py` (`step_left`).
