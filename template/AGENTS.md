# Agent instructions

<!-- cordee -->
## Cordee

This repo uses [Cordee](https://github.com/GrIc/cordee-harness). Read [cordee/README.md](cordee/README.md) (this
project), [cordee/WORKFLOW.md](cordee/WORKFLOW.md) (how a change is made) and
[cordee/coding-style.md](cordee/coding-style.md) first. Intent governs purpose; code and tests establish facts. Once the
code and its tests are written, read the whole diff (step 4 of COMPILE), then run `bash cordee/bin/cordee next` and do
what it says, again and again, until it says to hand off.

What the harness gives you, besides the checks the workflow runs:

- `bash cordee/bin/cordee doctor` says what is out of date in this clone, and prints what a bug report about the harness
  needs: do what its NOTE lines say, and paste it in the report.
- `bash cordee/bin/cordee quiet <command>` prints one line when a command passes, its end when it fails.
- `bash cordee/bin/cockpit report "$PWD"` shows where this dev's tokens went:
  [cordee/guide/tokens.md](cordee/guide/tokens.md).
- A guide for each rarer case (first batch, plan, upgrade), listed at the top of the workflow.
- When the dev types *quiz feedback*: read `QUIZ.md`, with what the dev ticked and wrote under each wrong question,
  and talk the questions through: where to look, as the hint says, never which box or why it is right. Propose a fix
  to the batch and, when a question or a guide is at fault, a change to the harness; make it only on a yes.

### How you work

Be lazy with effort, never with thought.

- Go straight to the goal: read only what the task needs, write the least code that does it, stop when it is done.
- No work nobody asked for: no extra refactor, option, test or document. Mention it in one line instead.
- Spend tokens like money: short answers, no restating.
- Fully transparent with the human: what you did, what you skipped, what you assumed, what you could not check.

### House rules

- One topic, one place; elsewhere, link. The order of the work lives only in `cordee/roadmap.md`.
- Reuse before building: the platform, then the framework, then a maintained library whose license and weight you
  checked; your own code last.
- Measure real input before specifying behavior that depends on it, and cite the numbers.
- Every claim cites its evidence: a `file:line`, a command and its output, or a measure. No evidence, no claim.
- Decisions of intent go to the human as short questions, with the data and a recommendation first. Decisions of fact
  you take yourself, and list in the handoff.
- Mark your work `Agent-Assisted: yes` in the proposed commit message. Never commit, push, bypass a hook, or tick
  `QUIZ.md`: the human does.
- The quiz's answers never reach the human before the commit: no reply, report or handoff gives a right box or why it
  is right, and only the agent that writes the quiz opens the key. A quiz answered with your help proves nothing.
- Fix a red main before anything else. Run the CI checks locally before proposing a batch.
- The harness runs on Python 3.10 or later: when a command says it is missing, tell the human how to install it.
- Each clone needs the hooks once: if `$(git rev-parse --git-path hooks)/pre-push` does not mention `cordee/bin/ledger`,
  run `bash cordee/bin/cordee install-hook` and tell the human.

### INTAKE, always

When the human mentions a bug, an idea or a constraint, even in passing: enrich its `cordee/issues/<slug>.md`, or create
one in a few lines (what, why, where it was seen). Say so in one line, then resume. "Someday X" is one line in
`cordee/roadmap.md` instead. Delete an issue once delivered; git keeps it.
<!-- /cordee -->
