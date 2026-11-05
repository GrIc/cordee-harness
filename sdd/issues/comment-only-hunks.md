# Hunks that only change comments count as code in the quiz

Seen on 2026-11-04, in Anthropic's write-up on Scion (https://www.anthropic.com/research/redesigning-source-control):
their review tool sets approval rules by what a change does, so a change of comments asks less than one of logic.

Why: `cover` (`template/sdd/bin/fabrik/quiz.py:114`) counts every hunk outside `NOT_CODE`
(`template/sdd/bin/fabrik/size.py:10`). A hunk that only edits comments or whitespace weighs as much in
`covers 5/7` as one that changes behavior, `audit` asks a high-risk quiz to cite it, and a batch of comments alone
still asks three questions.

First, measure: on the pilots' history and the kit's own, the share of agent-batch hunks that only change comments or
whitespace. Under a few percent, close this issue: comment syntax per language is code to keep for little. Whitespace
alone is cheap to spot (`git diff -w`).

Where: `quiz.cover` and the rule that spares a batch its quiz (`sdd/modules/checks.md`). Same direction as the roadmap
line on risk levels ("A batch of tests or docs only asks less").
