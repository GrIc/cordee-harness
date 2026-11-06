# 3.2: what the first field use broke, a batch the script leads, and settings in one place

Why: on the first demo with opencode and Qwen, a batch of Markdown and a `.gitignore` was refused for want of a quiz
nobody expected, and the agent wrote its deny list in a format opencode ignores. Teams start on Monday with Kilo Code
and Copilot, and want to set the batch size and the risk for the repo at setup and for a module when it is created,
instead of editing the kit's scripts, which an upgrade replaces. On a first try with Kilo Code and a light model
(2026-11-05), the agent wrote the code and the tests, then handed off without staging, writing the message, running
the audit or calling a reviewer; light models are what the teams will run. A dev with a good reason to skip the quiz
can only do it today by leaving out the agent's trailer or `--no-verify`, which leaves no trace of why.

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
