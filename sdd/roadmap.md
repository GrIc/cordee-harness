# Roadmap

- More settings in `sdd/config.yml`: the roles present, the quiz type each role gets and when, who answers for a
  missing role, the default checkpoint (commit or merge request); a contract states the levels it touches and its
  checkpoint only where they differ from the project's.
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
