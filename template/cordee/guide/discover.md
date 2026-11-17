# Discover: code that lived before the harness (for agents)

When the harness comes to a repo with its history, at deploy or at the first batch in a zone nobody mapped: read wide
and cheap, write only what the next batches need, and let the contracts catch up batch after batch.

## Once, at deploy

1. `bash cordee/bin/cordee discover` sums the tracked code by folder, with how much a contract governs and the prose
   beside it; `discover <folder>` goes one level down. Read the prose first: the README, the contribution guide, the
   team's `AGENTS.md`, the architecture and decision records. Then the files that say how the code is checked: the
   build files of each stack, the hook manager, the CI. Open code only where the prose is silent, entry points first.
2. Write the map in `cordee/README.md`: the system in a few lines, then one row per zone the dev will work in (its
   folder, what it does, its stack, who owns it), linking the team's documents instead of restating them. A zone
   nobody plans to touch gets no row.
3. Write `cordee/coding-style.md` from what the team enforces, not from what the kit proposes: the commands that
   format, lint, test and build each stack, the commit message and branch conventions (`git log -30 --format=%s`
   shows them), the review rules. Where the team's rule and the kit's differ, the team's wins.
4. Ask the dev the settings of `cordee/config.yml` as [start.md](start.md) says. A zone that needs its own
   `batch-lines` or `risk` gets a contract with its folder in `governs` and the setting in its front matter; a
   module inside it may set its own again.

Stop there: no contract for code no batch is about to change.

## Then, with each task

- Before a batch changes code no contract governs, write that contract, from the code and its tests as step 1 of
  [learn.md](learn.md) says, governing the smallest folder that holds the intent. `audit` names such code: `NOTE
  <file>: code in no module`. Code whose intent is plain from its tests may stay without one.
- A task larger than a batch (a ticket, a PRD) follows [plan.md](plan.md): each section names its module, and a
  module without a contract gets it with the first batch that touches it.
- A team document that changed since the map was written wins over it: update the row or the contract in the batch
  that meets the difference.
