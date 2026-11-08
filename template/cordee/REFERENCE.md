# Cordee reference manual

This manual is the complete reference for developers and teams using Cordee. For a quick daily cheat sheet, see
[GETTING-STARTED.md](GETTING-STARTED.md). The instructions agents read at each batch live in [WORKFLOW.md](WORKFLOW.md).

## 1. Stance and design principles

- Pace follows comprehension, never generation. Agent code enters git history only once a human has read the diff and
  answered a short predictive quiz on what the batch changes.
- Intent lives in short contracts (`<= 50` lines); implementation facts (SQL shapes, file layouts, JSON schemas) stay
  in code and tests.
- Incentives, never locks. Every check can be bypassed with an explicit reason recorded in git history
  (`Spec-Unchanged(<module>): <reason>`, `Large-Batch: <reason>`, `Bypass-Quiz: <reason>`), and a human's own commits
  only receive warnings on drift and size.
- Measure the product, never the people. When the optional token module is enabled (`tokens: true`), token spend is
  summed by module and month in anonymous git notes (`refs/notes/cordee-ledger`), with no commit hash, no author, and
  no day. What the quiz learns about a developer never leaves their machine.

## 2. Repository layout and file ownership

Files owned by the kit are replaced cleanly whenever `cordee deploy` upgrades the repository. Project-owned files are
never overwritten by an upgrade:

| Path | Owner | Purpose |
|---|---|---|
| `cordee/bin/cordee` | Kit | Core CLI launcher (drift, size, quiz, `brief`, `next`, `quiet`, `doctor`, `deploy`). |
| `cordee/bin/cockpit`, `cordee/bin/ledger` | Kit | Optional launchers for local token breakdown/hints and anonymous team ledger. |
| `cordee/bin/harness/` | Kit | Python 3.10+ standard-library package run by the launchers. |
| `cordee/WORKFLOW.md`, `cordee/guide/` | Kit | Agent workflow and on-demand guides (`start`, `plan`, `tokens`, `upgrade`, `from-sdd-fabrik`). |
| `cordee/GETTING-STARTED.md`, `cordee/REFERENCE.md` | Kit | Developer quick-start guide and this reference manual. |
| `AGENTS.md` (`<!-- cordee -->` block) | Kit | Agent instructions block, updated in place by `cordee deploy`. |
| `cordee/README.md` | Project | System map and module table (line 1 tracks `Deployed from <source> <tag>.`). |
| `cordee/config.yml` | Project | Repository-wide settings (comments show defaults). |
| `cordee/coding-style.md` | Project | Code, test, documentation and commit conventions, plus project check commands. |
| `cordee/modules/<module>.md` | Project | Module contracts (`<= 50` lines), created as modules appear. |
| `cordee/{product,design,architecture,decisions,roadmap}.md` | Project | Topic files created when first needed; `decisions.md` is numbered with `Rejected:` lines. |
| `cordee/changes/<slug>.md` | Project | Multi-batch plans, shrunk as batches land and deleted when delivered. |
| `cordee/issues/<slug>.md` | Project | Bugs and ideas caught in passing (INTAKE), deleted when delivered. |

## 3. Configuration (`cordee/config.yml` and contract front matter)

`cordee/config.yml` sets repository defaults using flat `key: value` lines (or `- item` lines below list keys). A
module contract's YAML front matter (`---` ... `---`) can override `batch-lines` and `risk`, and add to `sensitive`,
for batches touching that module.

| Setting | Scope | Default | Description |
|---|---|---|---|
| `tokens` | Repo | `false` | Enables the cockpit and the token ledger. When `false`, `install-hook` writes only `commit-msg` and `post-commit` (`committed`), with no `pre-push` network hook. When `true`, `install-hook` adds `ledger record` to `post-commit` and `ledger sync` to `pre-push`, and `cordee hints` at handoff adds the cockpit's cost hints. Run `bash cordee/bin/cordee install-hook` after changing it. |
| `batch-lines` | Repo, Contract | `200` | Maximum changed non-blank lines of code and tests in an agent batch. Up to 5% over prints a `NOTE` without blocking; above 5% refuses an agent batch unless `Large-Batch: <reason>` is in the commit message. A contract's `batch-lines` replaces the repo's when that module's governed code changes (if multiple coded modules set it, the lowest wins). Changing `batch-lines` applies immediately to the batch and prints a `NOTE`. |
| `risk` | Repo, Contract | `normal` | Quiz requirement: `none` (no quiz on code), `normal` (1 to 3 questions), or `high` (3 or more questions whose `See` lines cite every changed hunk of code, with a second human's reading recommended). A batch is judged at the highest risk of the modules it touches in the parent or the batch; code outside every module uses the repo's risk. |
| `sensitive` | Repo, Contract | Kit list | Paths (`path/to/file`), folders (`folder/`), or regular expressions (`/pattern/`) that always require a quiz (at least `normal` risk), even when `risk: none` or when only Markdown changed. Setting `sensitive` in `cordee/config.yml` replaces the kit's list (`sensitive: []` empties it); a contract's `sensitive` list adds to the repo's. |
| `not-code` | Repo | Lock files | Paths, folders, or `/regex/` excluded from both `batch-lines` and quiz hunk coverage (in addition to Markdown and `.gitignore`, `.gitattributes`, `.gitkeep`). Setting it in `cordee/config.yml` replaces the default lock-file patterns (`/\.lock$/`, `/lock\.json$/`, `/lock\.yaml$/`). A batch that widens `not-code` is still judged against the parent's list. |
| `agent-emails` | Repo | Kit list | Co-author email addresses (`noreply@anthropic.com`, `noreply@openai.com`, `aider@aider.chat` by default) that mark a commit as agent-assisted. Setting it in `cordee/config.yml` replaces the kit's list; a batch that removes an address is still judged by the parent's list. |
| `review-wait-hours` | Repo | `4` | Age in hours after which `cordee brief` reports an unmerged remote branch from a teammate as waiting for review. |
| `abandoned-days` | Repo | `14` | Age in days after which `cordee brief` stops reporting an unmerged remote branch. |

## 4. Module contracts (`cordee/modules/<module>.md`)

A contract states what a module promises and links each criterion to the tests that prove it:

```markdown
---
governs: [src/search.py, src/templates/search/, tests/test_search.py]
depends: [tags]
risk: high
batch-lines: 150
---
# search

Intent, constraints and non-goals, then the criteria.

- A misspelled term of 4 letters or more is corrected to the closest name:
  [test_corrects_a_misspelled_term](../../tests/test_search.py).
```

Rules enforced by `cordee audit` and the commit hook:

- `governs` is required and non-empty. It accepts inline bracket lists (which may wrap across lines), `- path` lines,
  or a single scalar path, always relative to the repository root.
- Drift check: if a batch changes any file matched by a module's `governs`, it must also update that module's contract
  or include `Spec-Unchanged(<module>): <reason>` in the commit message.
- Link verification: every Markdown link `[text](target)` in a contract (except web URLs and links to `.md` files or
  directories ending with `/`) must resolve to an existing file in the commit. If `text` is neither the file's basename
  nor its path, `text` must appear as whole words inside that file (for example, a test function or class name).
- Guidance (`NOTE`, never blocks): `cordee audit` notes any `governs` pathspec that matches no tracked file, and reports
  the ratio of project Markdown lines to governed code lines (excluding kit docs, the `AGENTS.md` block, and unsettled
  template rows in `cordee/coding-style.md`).

## 5. Batch workflow, review, and quiz

### 5.1 Before and during the batch

1. `bash cordee/bin/cordee brief [<module>]` checks up to three items waiting for the developer (an unanswered
   `QUIZ.md` in another worktree of the clone, or teammate remote branches not merged into `origin/HEAD` between
   `review-wait-hours` and `abandoned-days` old, ignoring bots). When given `<module>`, it also reports if this is the
   developer's first commit touching that module and names the three teammates who delivered there most, so the agent
   can offer discovery mode.
2. The agent builds a single-module change within `batch-lines` (blank lines and pure file renames count as zero lines;
   text files marked `binary` or `-diff` in `.gitattributes` still count), runs the project's test suite (using
   `bash cordee/bin/cordee quiet <command>` when the runner is verbose), and updates the contract.
3. The agent runs `bash cordee/bin/cordee next`, which inspects git state and prints the exact step of `COMPILE` left
   (staging files, writing `.git/cordee/message`, fixing drift or size findings, spawning the reviewer for `QUIZ.md`,
   or handing off), plus any out-of-date hooks or untracked files.

### 5.2 Fresh review and `QUIZ.md`

A fresh reviewer agent context inspects the staged diff against the contract and coding style, reports evidence-backed
findings, and writes `QUIZ.md` at the repo root plus the answer key at the path printed by
`bash cordee/bin/cordee fingerprint`.

- Each question asks the human to predict behavior or intent from the lines cited on its `See` line (`file:line` or
  `file:line-line`, up to three places separated by `, `), without chasing a change across other files:
  - code changes: what a function returns for a given input, which line enforces a rule, what breaks if a line is
    removed, or why an approach was chosen;
  - contract or `product.md` changes: what promise changes;
  - `depends`, `governs`, or `architecture.md` changes: how the structure changes;
  - test-only batches: what a test pins and what it misses;
  - `decisions.md`: what option was rejected and why.
- Each question has 2 to 4 `- [ ]` options, with the right box varied across questions. Everything the human reads is
  written in their language.
- On commit, the `commit-msg` hook grades `QUIZ.md` offline against the key and appends `Quiz: <n>/<n>, covers <c>/<t>`
  to the commit message, where `<c>/<t>` is the number of changed code hunks in `git diff --cached -U0` whose line
  range overlaps a `See` range.
- Once the commit succeeds, `post-commit` (`bash cordee/bin/cordee committed`) records any question the developer
  flagged or commented into `$(git rev-parse --git-common-dir)/cordee/quiz-journal` (local to the machine, shared
  across worktrees) and removes `QUIZ.md` and the key. If a quiz is replaced before any commit, for a reworked batch or
  for the same one, the next `fingerprint` run journals those flags too.

## 6. Commit trailers

| Trailer | Author | Effect |
|---|---|---|
| `Agent-Assisted: yes` | Agent (or hook when a matching quiz key exists) | Enforces drift, size, and quiz checks on the commit. |
| `Spec-Unchanged(<module>): <reason>` | Agent or human | Spares `<module>` from the contract drift check and from the single-module limit (its changed lines still count toward `batch-lines`). |
| `Large-Batch: <reason>` | Human | Lifts both size limits (`batch-lines` and the single-module limit) while printing a `NOTE`. |
| `Bypass-Quiz: <reason>` | Human (never the agent) | Skips the quiz even at `risk: high`; drift and size checks still apply. |
| `Quiz: 3/3, covers 5/7` | `commit-msg` hook | Records the passed quiz and its hunk coverage. |

## 7. Optional module: Cockpit and Token Ledger (`tokens: true`)

By default (`tokens: false` in `cordee/config.yml`), Cordee runs in core-only mode: no token logs are read by hooks
and no `pre-push` network hook is installed. Even if `cordee/bin/cockpit`, `cordee/bin/ledger`, and their Python modules
are deleted, all core commands continue to work.

To enable the cockpit and token ledger for the repository, set `tokens: true` in `cordee/config.yml` and run
`bash cordee/bin/cordee install-hook`.

### 7.1 Local cockpit (`cordee/bin/cockpit`)

Reads local agent logs on the developer's machine (Claude Code, opencode, and Kilo Code) without sending anything over
the network:

- `bash cordee/bin/cockpit report "$PWD" [<since> <until>]`: over the developer's last 10 agent batches by default,
  reports Claude Code's exact cost in input-equivalent tokens by role (`writer`, `reviewer`, `agent:<type>`) and exact
  model, median starting context for sessions and sub-agents, longest context reached, cache-read share, and estimated
  cost of attachments sent along with calls (tool results, skill listings, hooks, MCP instructions, memory files).
- `bash cordee/bin/cockpit hints`: run by `cordee hints` at handoff when `tokens: true`; prints a hint at most once
  per 10 agent batches when MCP servers or plugins go unused above the cost threshold, when context exceeds 150k
  tokens, or when a log format change prevents reading replies or token counts.

### 7.2 Anonymous team ledger (`cordee/bin/ledger`)

Tracks what each product module costs in tokens per month, never per developer:

- `post-commit` runs `bash cordee/bin/ledger record`, which queries `cockpit usage` since the last recorded commit and
  splits the token counts across the modules touched by `HEAD` (or `-` outside modules) into a git note in
  `refs/notes/cordee-ledger`, attached to a random object hash and dated the first of the month with author `cordee`.
- `pre-push` runs `bash cordee/bin/ledger sync [<remote>]`, which fetches and merges `refs/notes/cordee-ledger` from
  the remote and pushes the result as a single parentless commit (so the shared history never reveals whose note came
  first), only when the local ledger tree has changed since the last sync with that remote.
- `bash cordee/bin/ledger report` sums tokens by month, module, role, and exact model, and shows the share of agent
  commits covered each month.
- Any developer can opt out locally at any time with `git config cordee.ledger false` (`--global` for all repositories).

## 8. CLI command summary

| Command | Description |
|---|---|
| `bash cordee/bin/cordee audit [--message <file> \| --range <base>..<tip>]` | Run drift, link, size, quiz form, and markdown ratio checks on the staged batch or a commit range. |
| `bash cordee/bin/cordee brief [<module>]` | Show waiting quizzes in other worktrees, teammate branches waiting for review, and first-time module info. |
| `bash cordee/bin/cordee next` | Print the next step of `COMPILE` from git state, plus stale hooks and untracked files. |
| `bash cordee/bin/cordee fingerprint` | Print the staged batch fingerprint and quiz/key paths, journaling any replaced quiz flags. |
| `bash cordee/bin/cordee install-hook` | Install `QUIZ.md` in `.git/info/exclude` and write the active git hooks (`commit-msg`, `post-commit`, and `pre-push` when `tokens: true`). |
| `bash cordee/bin/cordee quiet <command>...` | Run a command, printing one summary line on success or the last 30 lines on failure. |
| `bash cordee/bin/cordee doctor` | Print version, environment, hook status, token/ledger status, and audit timing, with `NOTE` lines for anything to fix. |
| `bash cordee/bin/cordee hints` | At handoff, name a module whose quiz answers were flagged *unclear* or *not-wanted* twice in the last 10 batches, then the cockpit's cost hints when `tokens: true` (each at most once every 10 batches). |
| `bash cordee/bin/cordee touched [<commit>]` | List the modules changed by `<commit>` (`HEAD` by default) with their changed line counts. |
| `bash <kit>/template/cordee/bin/cordee deploy <source> <tag> [--forge github\|gitlab]` | Deploy or upgrade Cordee from a kit clone into the current repository. |
| `bash cordee/bin/cockpit report <repo> [<since> <until>]` | Show local Claude Code token breakdown and attachment overhead. |
| `bash cordee/bin/cockpit hints` | Print actionable cost hints (at most once every 10 batches). |
| `bash cordee/bin/ledger report` | Show monthly anonymous token spend per module, role, and model, plus batch coverage. |
