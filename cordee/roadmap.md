# Roadmap

## Fixes

- [The ledger finds no opencode session on Windows](issues/opencode-windows-paths.md).
- [Split test/run by module](issues/split-test-run.md).
- [The proposed commit message file persists after commit](issues/clean-message-file.md).
- [Trailing whitespace or inverted spans break the See line check](issues/quiz-see-whitespace.md).
- [The tokens setting in config.yml is never validated](issues/tokens-config-validation.md).
- [Claude Code log reader scans entire history on every commit](issues/claude-logs-mtime.md).
- [The quiz key reveals answers in plain text](issues/hashed-quiz-key.md).
- [Quiz answers follow predictable patterns](issues/random-quiz-answers.md).
- [A wrong answer is fixed by ticking another box of the same question](issues/retry-same-question.md).
- [The format guard does not see a renamed attachment](issues/attachment-format-guard.md).
- [The cockpit's tests read only logs the kit wrote](issues/real-log-excerpts.md).

## Then

- CI sums up a merge request from its commits' trailers (quizzed, bypassed with a reason, the human's own, an agent's
  with neither quiz nor reason, as `--no-verify` leaves it), with no quiz of its own.
- A relay quiz: the dev who takes over a module answers the quiz of its last batches.
- [Hunks that only change comments count as code in the quiz](issues/comment-only-hunks.md).
- A queue of slow decisions: a reversible one is taken as provisional with a review date, its age shown by `brief`.
- Copilot Chat (the classic VS Code extension) in the cockpit, specified from a team's real logs.
- Someday: publish the exchanges between humans and agents (quiz feedback, hints, trailers) as an open protocol, so
  that a team or a tool can adopt it without the kit.
