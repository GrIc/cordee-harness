# Developing Cordee

- `template/` is what lands in user repos. Edit it; never copy it elsewhere in the kit.
- The kit follows its own rules and runs its own harness: `template/AGENTS.md`, `template/cordee/WORKFLOW.md` and
  `template/cordee/coding-style.md` apply here, `cordee/bin/cordee` runs the template's script, and its contracts are
  `cordee/modules/checks.md` and the modules it links.
- Rules the coding style leaves to settle, for the kit: no formatter or linter, two-space indents (PEP 8 in Python),
  120 columns, snake_case functions, an error says what to do next, the command dispatch last (bash defines before it
  calls).
- Run `bash test/run`, `bash test/ledger` and `bash test/cockpit` before proposing a batch, each through
  `bash cordee/bin/cordee quiet`, which prints one line when it passes.
- `docs/feedback/` is local input from field use: read it, never commit it.
- Decisions about the kit go to `docs/decisions.md`, with a `Rejected:` line.
- Never commit, push or tag: the human does.
