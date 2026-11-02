# SDD-Fabrik workflow

How a change is made in this repo. This file and `guide/` belong to [SDD-Fabrik](https://github.com/GrIc/sdd-fabrik)
and are replaced on upgrade: project rules go in [coding-style.md](coding-style.md) or in `AGENTS.md` outside the kit
block.

Read a guide only when its case comes:

- a new project, or existing code to adopt, as the first batch: [guide/start.md](guide/start.md);
- work of several batches: [guide/plan.md](guide/plan.md);
- what agents spend, by module and for each dev: [guide/tokens.md](guide/tokens.md);
- upgrading or removing the kit: [guide/upgrade.md](guide/upgrade.md).

## Where things live

A file is created when first needed.

| Topic | Home |
|---|---|
| The project's map: system, modules | `sdd/README.md` |
| Why, for whom, success, non-goals | `sdd/product.md` |
| Look, accessibility, voice | `sdd/design.md` |
| Code, tests, docs and commit conventions, project commands | `sdd/coding-style.md` |
| System design, data, deployment | `sdd/architecture.md` |
| Decisions, with what was rejected | `sdd/decisions.md` |
| Order of the work, someday | `sdd/roadmap.md`: one line and link per change, and nowhere else |
| A piece of work in several batches | `sdd/changes/<slug>.md`, deleted once delivered |
| What a module must do, its acceptance | `sdd/modules/<module>.md`, linked to the tests that prove it |
| Bugs and ideas caught in passing | `sdd/issues/<slug>.md` |
| Implementation facts | code and tests |

## COMPILE: one batch

1. Read the intent, the contract, its tests and the code. Ask the open intent questions. When behavior depends on real
   input, measure it with a throwaway script first, and stop at the approach that covers 95 to 98% of real cases.
   Run `bash sdd/bin/sdd brief <module>`. When it shows what waits, a quiz in another worktree or a branch waiting for
   a review, propose to finish that before producing more. When it says this is the dev's first batch there, offer a
   discovery mode and apply it only on a yes: sum up the contract and its decisions, ask the dev how they would go
   about it, keep the batch small, tell the reviewer so that its quiz asks why rather than which line, and suggest
   pairing with one of the devs it names.
2. Build the smallest coherent change, with the tests it deserves ([coding style](coding-style.md#tests)). Run the
   project's checks. Never cut a user text, a test or a name to fit the size limit: split the batch, or ask the human
   for `Large-Batch`.
3. Update the contract if the intent changed. An intent that goes against `sdd/decisions.md`, even at the human's
   request, comes with a new decision that supersedes the old one. A batch from a plan moves its criteria into its
   module's contract, in place of what they restate, and deletes its section; a batch without a module drops them.
   Otherwise propose `Spec-Unchanged(<module>): <reason>`.
4. Read the whole diff against the coding style and delete what does not earn its place.
5. Stage the batch, write the proposed message with `Agent-Assisted: yes` to `.git/sdd/message`, and run
   `bash sdd/bin/sdd audit --message .git/sdd/message`.
6. Review: spawn a fresh reviewer, a new context that did not write the batch. It reads the staged diff, the contract
   and the coding style, and reports findings with their evidence. Once they are fixed, it writes the quiz, then runs
   the audit of step 5 again, which checks the quiz. Give it a smaller model than the writer's unless the batch is
   large or touches security or data. After a fix, send the same reviewer the change: it checks that its quiz still
   holds for a fraction of a fresh one.
7. Hand off: purpose, the decisions you took alone, evidence, limits and a short "understand this" for the human, and at
   high risk the advice to have a second human read the diff. The human reads the diff, answers `QUIZ.md` and commits
   with `git commit -F .git/sdd/message`. Start the next batch in a fresh session: a long one reads its whole history
   again with every call. Then run `bash sdd/bin/cockpit hints`: it prints a line only when this dev's costs show
   something new to cut, or their quiz answers in a module were flagged twice. Put each to the human as a question,
   with the change you would make (turn off a plugin or an MCP server, fold an output, write a rule in the contract, the
   coding style or the quiz instructions), and make it only on a yes, in a batch of its own.

Wherever a fresh reviewer is asked for (plan, batch, module), a tool that cannot spawn one does its part itself and
says so; one that cannot pick a model or resume a sub-agent skips that.

## Quiz

How many questions depends on the risk. A batch whose changed files are all Markdown outside `sdd/modules/` needs no
quiz (one written is still graded). A batch that changes a module declaring `risk: high` (an API contract, security,
personal data, money) needs five, and the handoff recommends a second human's reading; nothing requires one, so a dev
alone uses the whole harness. Any other batch needs three.

`bash sdd/bin/sdd fingerprint` prints the batch fingerprint and the two paths to write. The reviewer writes:

- `QUIZ.md` at the repo root (kept out of git): questions that make the human predict, not recognize. What does
  this return for that input, which line enforces this rule, what breaks if this line goes, why this option over that
  one. Each question cites a changed `file:line` and has 2 to 4 boxes; the right box changes place.

  ```markdown
  # Quiz for this batch

  Tick one box per question, save, then commit.

  ## 1. What does parse_duration return for "2 hours 30"?

  See src/durations.py:14

  - [ ] 150 minutes
  - [ ] 2 hours
  - [ ] an error
  ```

- the key, at the printed path: the fingerprint, then one line per question with the right letter (A for the first
  box) and a hint for a wrong answer: where to look, never which box. No question asks for a computation nobody does
  when reading code.

  ```
  3f2a9c...
  A "30" after hours counts as minutes.
  ```

The commit fails until every answer is right. Under each wrong question, the hook writes a quoted block in
`QUIZ.md`, once: the hint, a call to type *quiz feedback*, and optional boxes for the dev to say why (not understood,
question unclear, the code does not do what they wanted). The boxes never change the grade. If the batch changed
since the quiz was written, the hook only warns: ask for a new quiz when the changes touch what it asks.

When the quiz passes, each question the dev flagged or commented goes to
`$(git rev-parse --git-common-dir)/sdd/quiz-journal`, on this machine only and shared by the clone's worktrees: one
tab-separated line, `v2`, the time in epoch seconds, the batch's modules (joined by `,`, or `-`), the boxes ticked
(`not-understood`, `unclear`, `not-wanted`, joined by `,`, or `-`), the question's title and the dev's own words (or
`-`). The cockpit reads it.

## Contracts

```markdown
---
governs: [src/search.py, src/templates/search/, tests/test_search.py]
depends: [tags]
risk: high
---
# search

Intent, constraints and non-goals, then the criteria.

- A misspelled term of 4 letters or more is corrected to the closest name:
  [test_corrects_a_misspelled_term](../../tests/test_search.py).
```

Govern the code that carries the intent: leave CI, dependency and build files out unless the module is about them.
At most 50 lines. Intent, never facts that a refactor keeping the behavior would change (SQL shapes, file layouts,
JSON formats). A criterion is a plain sentence, then links to the tests that prove it: a test name, a group, or the
whole file with its name or path as the link text, relative to the contract or from the repo root. Several criteria
may share a test; a criterion without a link is checked by hand, as its sentence says. No checkboxes, no status.
`depends` names the modules this one builds on; check their tests pass before you do. `risk: high`, for a module where
a mistake costs much (an API contract, security, personal data, money), asks for a stricter quiz.

## Decisions

`sdd/decisions.md`, numbered. Each entry gives the choice, its evidence, and a `Rejected:` line with the alternatives
and why. Numbers never change and no entry is deleted: a superseded entry shrinks to `n. Superseded by m.`, and git
keeps its text.

## Commit trailers

| Trailer | Written by | Effect |
|---|---|---|
| `Agent-Assisted: yes` | the agent, in its proposed message | drift and size block, the quiz is required |
| `Spec-Unchanged(<module>): <reason>` | the author | spares that module from the drift check and the one-module limit |
| `Large-Batch: <reason>` | the human | lifts the size limits (`MAX_LINES` in `sdd/bin/sdd`, one module) |
| `Quiz: 3/3` | the hook | records the passed quiz and its number of questions |

A co-author address listed in `AGENT_EMAILS` (top of `sdd/bin/sdd`) counts as `Agent-Assisted: yes`; any other commit
is the human's own. The script prints ERROR when every commit must stop; DRIFT (code against its contract, or a
contract link to a missing test or file) and SIZE (more than 5% over `MAX_LINES`, or a second module), which refuse an
agent batch and only warn on the human's own; and NOTE, guidance that never refuses. CI replays drift and size on every
pushed commit, never the quiz. Everything here can be bypassed: it is there to help, not to lock.

The hook compares the batch with HEAD: to amend an agent batch that changes files, run `git reset --soft HEAD^` and
commit again. Merge pull requests with a merge commit or a rebase: a squash adds the batches up, so the size check
fails on the default branch, or it drops their trailers.
