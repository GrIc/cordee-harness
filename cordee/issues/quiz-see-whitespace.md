# Trailing whitespace or inverted spans break the See line check

Seen on 2026-11-09 during review: `quiz.questions()` only removes leading spaces on the `See` line with
`line[4:].lstrip(" ")`. If a reviewer model emits a trailing space (`See a.py:4 `), `span` becomes `"4 "` which fails
`re.fullmatch(r"[0-9]+(-[0-9]+)?", span)`. Furthermore, an inverted span such as `a.py:20-10` is not rejected by `form()`,
leading to `first > last`.

Why: Reviewer sub-agents occasionally append trailing whitespace to lines, triggering an opaque refusal on a line that
looks visually correct.

Leads:
- Use `.strip(" ")` instead of `.lstrip(" ")` when parsing `See` lines.
- Validate that `int(first) <= int(last)` in `form()`.

Where: `template/cordee/bin/harness/quiz.py` (`form`, `questions`).
