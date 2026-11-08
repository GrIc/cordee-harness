# The quiz's answers reach the human through the agents

Seen on 2026-11-08 on `9852c39`: an agent that fixed the quiz gave its right letters, and why one was right, in its
handoff. The human committed a quiz that proved nothing. Same batch, before: Kilo's reviewer told the writer each
right answer in its report, and the writer printed the key with `cat` while checking the state.

Nothing in the workflow forbids it: step 6 has the reviewer report its quiz to the writer, step 7 lists what the
handoff holds but not what it must leave out, and `AGENTS.md` only forbids ticking `QUIZ.md`.

Lead: the reviewer reports the number of questions and the audit, never the letters; the handoff and every reply
keep the key's content out until the commit; a house rule says so in `AGENTS.md`.

Where: `template/sdd/WORKFLOW.md` steps 6 and 7, `template/AGENTS.md`.
