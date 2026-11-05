# 3.2: what the first field use broke, a batch the script leads, and settings in one place

Why: on the first demo with opencode and Qwen, a batch of Markdown and a `.gitignore` was refused for want of a quiz
nobody expected, and the agent wrote its deny list in a format opencode ignores. Teams start on Monday with Kilo Code
and Copilot, and want to set the batch size and the risk for the repo at setup and for a module when it is created,
instead of editing the kit's scripts, which an upgrade replaces. On a first try with Kilo Code and a light model
(2026-11-05), the agent wrote the code and the tests, then handed off without staging, writing the message, running
the audit or calling a reviewer; light models are what the teams will run. A dev with a good reason to skip the quiz
can only do it today by leaving out the agent's trailer or `--no-verify`, which leaves no trace of why.

## The human may skip the quiz with a reason (checks)

- A commit whose message carries `Bypass-Quiz: <reason>` passes the hook without a quiz and gets no `Quiz:` trailer;
  drift and size still apply, on a `risk: high` module too. The trailer stays in the commit: it is the trace.
- `Bypass-Quiz:` without a reason lifts nothing, and the hook says to write why after the colon.
- The workflow's Quiz section and its trailers table say it, written by the human only.

## The script says the next step of a batch (brief)

The command's line in `__main__.py` and its tests in `test/run` belong to checks: the batch carries
`Spec-Unchanged(checks)`.

- `bash sdd/bin/sdd next` prints `step <n>: <what to do>` from the state of the batch in git, the first that
  applies, and always exits 0:
  - nothing changed and nothing staged: nothing to propose;
  - tracked files changed but not staged, or no message at `$(git rev-parse --git-path sdd/message)`, or one older
    than the last commit: step 5;
  - the audit's findings, the drift ones as step 3, the others as step 5;
  - a batch that asks a quiz, without `Bypass-Quiz`, whose `QUIZ.md` is missing, malformed or older than the batch:
    step 6, a fresh reviewer, or the same one after a fix;
  - else: step 7, the handoff.
- Untracked files never block: `next` lists them, for the agent to stage those that belong to the batch.
- The kit block of `AGENTS.md` asks the agent, once the code and tests are written, to read the diff (step 4) and
  then run `next` and do what it says until the handoff; COMPILE names it too.

## A contract or sdd/config.yml sets a module's risk (contracts)

- `sdd/config.yml` holds flat `key: value` lines, comments allowed, the same as a contract's front matter; without it,
  the harness behaves as today.
- A setting is read from the contract's front matter, else from `sdd/config.yml`, else the kit's default.
- `risk: high` in `sdd/config.yml` puts every module that does not say otherwise at high risk; a contract's
  `risk: normal` keeps it at normal risk.

## sdd/config.yml sets the batch size of the repo (checks)

- `batch-lines` in `sdd/config.yml` sets the lines of code and tests an agent batch may change, 200 without it; the
  5% margin follows it. A batch is judged on the smaller of its parent's value and its own.

## A contract sets the batch size of its module (checks)

- A contract's `batch-lines` sets the limit of a batch that changes that module's code, the smaller of the
  module's and the repo's value.

## Settings are asked at setup and at a module's birth (no module)

- The deploy copies a `sdd/config.yml` with the defaults written as comments; GENESIS and ADOPT ask the human for
  the batch size and the risk and write what differs; a new contract states only what differs from the repo's.
- The upgrade guide stops asking to keep a project's change to `MAX_LINES` by hand: it goes to `sdd/config.yml`.
