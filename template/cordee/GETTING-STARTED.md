# Getting started with Cordee

This page covers what you will see at each batch, how to commit, the one-time settings for your clone and forge, and
what to do when the harness refuses a commit. For the full human reference, read [REFERENCE.md](REFERENCE.md); the
agent instructions live in [WORKFLOW.md](WORKFLOW.md).

## What happens at each batch

1. Your agent checks `bash cordee/bin/cordee brief <module>`, builds a small single-module batch (200 non-blank lines
   of code and tests at most by default), updates the module's contract in `cordee/modules/<module>.md`, and runs
   `bash cordee/bin/cordee next` until it says to hand off.
2. A fresh reviewer (a new agent context that did not write the batch) checks the staged diff against the contract and
   coding style, and writes `QUIZ.md` at the repository root: 1 to 3 predictive questions about what the batch changes
   (3 or more citing every hunk of code when `risk: high`, none at `risk: none` unless a `sensitive` file moved).
   Neither agent ever gives away a right box or why it is right before you commit.
3. You read the diff and the handoff, tick one box (`- [x]`) per question in `QUIZ.md`, save, and commit.
4. If an answer is wrong, the commit fails and a hint block appears under that question in `QUIZ.md`. Read the lines
   its `See` cites, fix your answer, save, and commit again. If a question is unclear or the code does not do what you
   wanted, tick the matching box under the hint and type `quiz feedback` to your agent: it will walk through where to
   look (never which box is right) and propose a fix to the batch or the rules.

The agent never commits, never pushes, never bypasses a hook, and never ticks `QUIZ.md`: you do. Start the next batch
in a fresh agent session so it does not re-read a long history on every call.

## How to commit

From a terminal:

```
git commit -F .git/cordee/message
```

From your IDE's Commit button, you can also type your own message: the hook recognizes an agent batch from its quiz
key and adds `Agent-Assisted: yes` itself. Prefer keeping the proposed message in `.git/cordee/message` when you can:
it states what the batch does and carries any `Spec-Unchanged(<module>): <reason>` trailer.

## One-time setup

- Hooks: each clone needs the git hooks once. If the agent did not install them, run
  `bash cordee/bin/cordee install-hook` (and `bash cordee/bin/cordee doctor` to verify). If you use Husky, Lefthook, or
  `core.hooksPath`, `install-hook` prints the lines to add to your hooks (`commit-msg` and `post-commit`, plus
  `pre-push` when `tokens: true` is set in `cordee/config.yml`).
- Forge merge strategy: disable squash merges on pull or merge requests, and choose "merge commit" or "rebase /
  fast-forward" in your project settings. Squashing adds all batches of a branch into one commit, which trips the size
  check on the default branch and drops per-commit trailers.
- Python 3.10 or later: required on your machine (`python3`, `python`, or `py -3`). On macOS, Apple's system `python3`
  is too old: install one from python.org or Homebrew. On Windows, use Git for Windows (which provides `sh`).
- Cockpit and token ledger (optional, enabled when `tokens: true` in `cordee/config.yml`): records anonymous monthly
  token spend per module in `refs/notes/cordee-ledger` on commit and syncs on push (Claude Code, opencode, Kilo Code,
  Antigravity CLI). To turn the ledger off on your machine: `git config --global cordee.ledger false`.

## When the harness refuses

| Message | What it means | What to do |
|---|---|---|
| `DRIFT <contract>: <path> changed, its contract did not` | Code in a module's governed paths changed without its contract. | The agent updates the contract, fixes the code, or adds `Spec-Unchanged(<module>): <reason>` to the commit message if behavior is unchanged. |
| `DRIFT <contract>: links "<name>" ...` | A link in the contract points to a missing file or a test name no longer in that file. | Fix the link target or test name in the contract. |
| `SIZE <n> changed lines of code and tests, over <limit>` | The batch exceeds `batch-lines` (200 by default) by more than 5%. | Split the batch, or add `Large-Batch: <reason>` to the commit message yourself. |
| `SIZE the batch changes code of <n> modules` | The batch touches governed code in more than one unspared module. | Split by module, spare a module whose behavior did not change with `Spec-Unchanged(<module>): <reason>`, or add `Large-Batch: <reason>`. |
| `QUIZ.md: question <n> has 0/2 boxes ticked. Tick one.` | A question has zero or multiple boxes ticked. | Tick a single `- [x]` box per question and save `QUIZ.md`. |
| `Question <n> is wrong: read the hint in QUIZ.md.` | A quiz answer does not match the key. | Read the hint block in `QUIZ.md` and the lines `See` cites, fix your box, and commit again (or type `quiz feedback`). |
| `QUIZ.md cites <c> of <t> hunks of code; at high risk...` | In a `risk: high` module, `audit` requires `See` lines to cover every changed code hunk. | Ask the reviewer agent to update `QUIZ.md` so every hunk is cited. |
| `Bypass-Quiz needs a reason after the colon` | `Bypass-Quiz:` was added without a reason. | Write a reason after the colon (`Bypass-Quiz: <reason>`) to skip the quiz while keeping drift and size checks. |
| `ERROR ...` | A malformed contract, `cordee/config.yml` setting, or `Spec-Unchanged` module name. | Stops both human and agent commits; follow the fix printed in the error message. |

## Good to know

- Amending an agent batch that changes files: `git commit --amend` compares the staged tree against the commit being
  amended (`HEAD`) rather than its parent. Run `git reset --soft HEAD^`, adjust your files, and commit again. (Amending
  only the commit message without changing files passes without a new quiz.)
- Reasons after `Spec-Unchanged(<module>):`, `Large-Batch:`, and `Bypass-Quiz:` are mandatory and stay in `git log`.
- Your own commits (without `Agent-Assisted: yes`, an agent `Co-Authored-By`, or a quiz key written for that staged
  tree) never ask a quiz, and drift or size findings only print warnings without blocking you.
- Diagnosis and bug reports: run `bash cordee/bin/cordee doctor` to check your hooks, version, and environment in one
  command.
