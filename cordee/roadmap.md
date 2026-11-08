# Roadmap

## Fixes

- [The ledger finds no opencode session on Windows](issues/opencode-windows-paths.md).
- `audit` caches `git show` by tree and path in `contracts.py`, if it takes over 3 s with 40 contracts on Windows.
- The reviewer asks reading questions (what it returns, which line, why this choice), never a counterfactual across
  files.
- [Split test/run by module](issues/split-test-run.md).
- [A wrong answer is fixed by ticking another box of the same question](issues/retry-same-question.md).
- [A flag is lost when the quiz is rewritten for the same batch](issues/unclear-flag-lost-same-batch.md).
- [The format guard does not see a renamed attachment](issues/attachment-format-guard.md).
- [The cockpit's tests read only logs the kit wrote](issues/real-log-excerpts.md).
- [A script that imports harness leaves __pycache__ in template/](issues/pycache-in-template.md).

## Simpler rules

- The quiz level says only how many questions: none, normal or high, plus the `sensitive` list, the reviewer setting
  the number; the step less for tests and the `intent` risk go first.
- The reviewer picks what each question is about from what the batch changes: behavior for code, the promise for a
  contract or `product.md`, the structure for `depends`, `governs` or `architecture.md`, what a test pins and misses
  for tests alone, the rejected option for a decision. The dev who commits answers them all.
- One install command for the mechanical part (copy without overwriting, hooks, exclude), the agent keeping only the
  merges.
- The cockpit and the ledger become an optional module: the core (drift, size, quiz, `next`) runs without them and
  without a network hook.

## Then

- CI sums up a merge request from its commits' trailers (quizzed, bypassed with a reason, the human's own, an agent's
  with neither quiz nor reason, as `--no-verify` leaves it), with no quiz of its own.
- A relay quiz: the dev who takes over a module answers the quiz of its last batches.
- [Hunks that only change comments count as code in the quiz](issues/comment-only-hunks.md).
- A queue of slow decisions: a reversible one is taken as provisional with a review date, its age shown by `brief`.
- Copilot in the cockpit, specified from its real logs.
- The ledger notes the exact model (`claude-opus-5-5`, not `opus`): the data an API of environmental impact needs,
  without the tooling to call it.
- Someday: publish the exchanges between humans and agents (quiz feedback, hints, trailers) as an open protocol, so
  that a team or a tool can adopt it without the kit.
