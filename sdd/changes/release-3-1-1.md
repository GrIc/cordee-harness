# 3.1.1: what the first field use broke, and settings in one place

Why: on the first demo with opencode and Qwen, a batch of Markdown and a `.gitignore` was refused for want of a quiz
nobody expected, and the agent wrote its deny list in a format opencode ignores. Teams start on Monday with Kilo Code
and Copilot, and want to set the batch size and the risk for the repo at setup and for a module when it is created,
instead of editing the kit's scripts, which an upgrade replaces.

## The deploy gives each tool's deny list (no module)

- Step 6 of "Deploy (for agents)" gives the exact deny rules for Claude Code, opencode and Kilo Code, and says that
  Copilot can only ask before such a command, never refuse it; for another tool, the agent writes no file it cannot
  find in that tool's documentation and tells the human.

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
