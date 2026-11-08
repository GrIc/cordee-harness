# Roadmap

## Fixes

- [Code marked binary escapes the size and the coverage](issues/binary-code-skips-size.md).
- A pure rename counts zero lines in the size: `size.py` reads the diff with `--no-renames`, so a rename counts twice.
- The Markdown ratio leaves out the kit's block in `AGENTS.md` and the "to settle" lines of the style template.
- [The journal may lose the feedback that led to a rework](issues/journal-loses-reworked-feedback.md).
- [A quiz outlives its commit once HEAD moves on](issues/stale-quiz-after-pull.md).
- [The ledger finds no opencode session on Windows](issues/opencode-windows-paths.md).
- The ledger syncs on push only when it holds notes the remote has not seen, not a fetch and a push every time.
- `audit` caches `git show` by tree and path in `contracts.py`, if it takes over 3 s with 40 contracts on Windows.
- The reviewer asks reading questions (what it returns, which line, why this choice), never a counterfactual across
  files.
- [Split test/run by module](issues/split-test-run.md).

## Simpler rules

- The quiz level takes three values (none, normal, high) plus the `sensitive` list, and the reviewer sets the number
  of questions; the step less for tests and the `intent` risk go first.
- One install command for the mechanical part (copy without overwriting, hooks, exclude), the agent keeping only the
  merges.
- The cockpit and the ledger become an optional module: the core (drift, size, quiz, `next`) runs without them and
  without a network hook.

## Then

- More settings in `sdd/config.yml`: the roles present, the quiz type each role gets and when, who answers for a
  missing role, the default checkpoint (commit or merge request); a contract states the levels it touches and its
  checkpoint only where they differ from the project's.
- Control at the merge request, architecture level: agents commit on their branch with the audit alone, a merge
  request carries one story, a fresh reviewer writes the quiz on the whole request, the configured role answers it,
  the merge commit carries the stamp and the CI checks it is there.
- A relay quiz: the dev who takes over a module answers the quiz of its last batches.
- A quiz per role, asked only when the change touches that role's level, with the fallback for a missing role.
- Functional level with the PO: the agent's scenarios set against the PO's intent when a story is planned and when
  its preview is accepted, without git for the PO.
- [Hunks that only change comments count as code in the quiz](issues/comment-only-hunks.md).
- A queue of slow decisions: a reversible one is taken as provisional with a review date, its age shown by `brief`.
- Run level by impact: a minor impact goes to the dev, a strong one to ops.
- Interface (UX) and tests (QA) levels.
- Kilo Code and Copilot in the cockpit, specified from real logs of each ([Kilo Code](issues/kilo-code-reader.md)).
- The ledger notes the exact model (`claude-opus-5-5`, not `opus`): the data an API of environmental impact needs,
  without the tooling to call it.
- Someday: publish the exchanges between humans and agents (quiz feedback, hints, trailers) as an open protocol, so
  that a team or a tool can adopt it without the kit.
