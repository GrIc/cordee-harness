# The quiz key reveals answers in plain text

Seen on 2026-11-10 during review: `.git/cordee/quiz-key` stores the right answer letter in plain text (`A Because of A...`).
A developer or agent can read all right answers with `cat $(git rev-parse --git-path cordee/quiz-key)` without reading the
diff or the cited lines.

Why: Decision 10 rejected hashed answers ("the hidden key is enough for an incentive"). In practice, an unhashed file is
too easy to inspect, either casually by a human or automatically by tools, defeating the comprehension check.

Leads:
- Store a hash of each question's correct answer rather than the raw letter: e.g. SHA-256 or HMAC computed over the batch
  fingerprint, the question number or title, and the right letter (such as `A`, `B`, `C`, `D`).
- The grader computes the hash of the developer's picked box and compares it to the stored hash.
- The hint remains readable so that `feedback()` can still insert it into `QUIZ.md` on a wrong answer without leaking the
  letter.

Where: `template/cordee/bin/harness/quiz.py` (`form`, `questions`, `grade`), and update `cordee/modules/quiz.md` and
`docs/decisions.md`.
