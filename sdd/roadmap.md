# Roadmap

- What [the review of 2026-11-02 left open](issues/review-leftovers.md), one batch each.
- A project config the kit never overwrites, written by the setup: the roles present, the quiz type each role gets
  and when, who answers for a missing role, the default checkpoint (commit or merge request), the batch size. The
  harness reads its settings there, not from constants. Today's settings stay the default, for a dev alone.
- The module contract says its risk in three values (low: drift only, normal: quiz, high: every part cited), the
  levels it touches and its checkpoint when it differs from the project's. A batch of tests or docs only asks less,
  never more than its module.
- The CI on GitLab, as on GitHub.
- Control at the merge request, architecture level: agents commit on their branch with the audit alone, a merge
  request carries one story, a fresh reviewer writes the quiz on the whole request, the configured role answers it,
  the merge commit carries the stamp and the CI checks it is there.
- A quiz per role, asked only when the change touches that role's level, with the fallback for a missing role.
- Functional level with the PO: the agent's scenarios set against the PO's intent when a story is planned and when
  its preview is accepted, without git for the PO.
- A queue of slow decisions: a reversible one is taken as provisional with a review date, its age shown by `brief`.
- Run level by impact: a minor impact goes to the dev, a strong one to ops.
- Interface (UX) and tests (QA) levels.
- Kilo Code and Copilot in the cockpit, specified from real logs of each.
- The ledger notes the exact model (`claude-opus-5-5`, not `opus`): the data an API of environmental impact needs,
  without the tooling to call it.
- Someday: publish the exchanges between humans and agents (quiz feedback, hints, trailers) as an open protocol, so
  that a team or a tool can adopt it without the kit.
