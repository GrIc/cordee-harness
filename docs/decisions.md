# Decisions

Numbers never change and no entry is deleted: a superseded entry shrinks to a line, and git keeps its text. Field
notes from the pilot (September 2026) and a second pilot (October 2026) are the evidence behind most entries.

## 1. A harness, not a kit of guides (2026-10-03)

Short guides plus sensors an agent meets without remembering them: a `commit-msg` hook and a CI step. The v1 kit was
1,700 lines of markdown and four protocols an agent had to remember to run; the pilot ran the method in about 270.
_Rejected:_ the four protocol files, the generated `SOURCE.md`, `last-sync` and `sync-repo`, dated audit reports.

## 2. One repo for spec and code (2026-10-03)

Drift is computed from the history that spec and code share. _Rejected:_ the detached topology (no shared history,
so drift becomes a ritual instead of a check).

## 3. Superseded by 40.

## 4. A native commit-msg hook (2026-10-03)

`install-hook` writes `.git/hooks/commit-msg` and never replaces a hook it did not write: it prints the line to add
instead. _Rejected:_ `core.hooksPath` (overrides the user's global hooks, such as a DCO check); pre-commit (decision 3).

## 5. The user's agent deploys it (2026-10-03)

The README tells an agent how to fetch a tag with git, copy without overwriting, merge an existing `AGENTS.md`, and
install the hook. _Rejected:_ an install script piped from curl (cannot merge what already exists); a manifest of raw
URLs to fetch one by one.

## 6. Kit files and project files apart (2026-10-03)

The kit owns `sdd/bin/`, `sdd/WORKFLOW.md`, `sdd/guide/` and a marked block of `AGENTS.md`; upgrade replaces them.
Everything else is the project's. _Rejected:_ one `sdd/README.md` mixing the workflow and the project map (every upgrade
conflicts).

## 7. Two weights: agents are blocked, humans warned (2026-10-03)

Constraints scale with how much of the change the human did not write. `Agent-Assisted: yes`, or a co-author address
listed in `AGENT_EMAILS` (Claude Code's, Codex's and Aider's), marks a batch. _Rejected:_ the same rules for every
commit (a human fixing a typo should not take a quiz); recognizing agents by name in `Co-Authored-By` (Claude is also
a first name, and "agent" shows up in human names and addresses); `Assisted-by:` as a mark (it can credit a human).

## 8. Drift per commit, waived per module (2026-10-03)

Each commit is checked against its parent; `Spec-Unchanged(<module>): <reason>` spares one module and says why in the
history. _Rejected:_ comparing the dates of the last commits on code and contract (a later contract touch hid an
earlier drift); a global `No-Spec-Impact` (7 in 19 pilot commits, exempting whole commits on free text).

## 9. Small batches, by count (2026-10-03)

An agent batch over 200 changed lines of code and tests, or touching more than one module, is refused unless the human
adds `Large-Batch: <reason>`. A module spared by `Spec-Unchanged` does not count: a file shared by two modules can
change for one of them. On the pilot, 10 of 12 code commits stayed under 160 lines; the two above were the hardest to
review. _Rejected:_ a guideline only; letting the agent judge its own batch (its `Spec-Unchanged` claims stand in the
message the human reads and commits). Up to 5% over only gets a note (2026-10-23): on the second pilot, an agent cut a
user text, a test case and a name to fit 200 lines; a higher `MAX_LINES` would only move the squeeze.

## 10. A quiz in a file (2026-10-03)

The reviewer writes `QUIZ.md` (boxes to tick) and a key hidden in `.git/`; the hook grades it. The human commits from a
terminal or an IDE button. _Rejected:_ questions asked on the terminal (no terminal behind IDE commit buttons, nor
reliably on Windows); hashed answers (the hidden key is enough for an incentive); free-text answers (fragile matching);
review attestations checked by CI (they forbid amend, rebase and squash-merge). A batch changed since its quiz
only warns (2026-10-07): refusing it cost an LLM call for each small edit.

## 11. No status, no checkboxes in contracts (2026-10-03)

Acceptance lives in test names, and a module is done when its tests pass. _Rejected:_ `status: compiled` (forgotten
for a day on two pilot modules); acceptance boxes that restate the specs. Acceptance now lives in contracts,
linked to the tests that prove it (2026-10-07, decision 20).

## 12. Flat, optional topic files (2026-10-03)

`product.md`, `design.md`, `architecture.md`, `decisions.md` and `roadmap.md` have fixed names and are created when
first needed. _Rejected:_ an `architecture/` folder; shipping empty files that read as true.

## 13. `CLAUDE.md` imports `AGENTS.md` (2026-10-03)

One line, `@AGENTS.md`. Claude Code reads `AGENTS.md` by itself only when there is no `CLAUDE.md`. _Rejected:_ no
`CLAUDE.md` (the first one a project adds would silently hide `AGENTS.md`); a symlink (checked out as a text file on
Windows by default); a sentence asking to read `AGENTS.md` (one more read to forget).

## 14. Deny lists set by the deploying agent (2026-10-03)

The agent adds `git commit`, `git push` and `--no-verify` to its own tool's deny list and says which agents only get
the instruction. _Rejected:_ shipping a `.claude/settings.json` (binds one tool only).

## 15. One builder, one fresh reviewer when possible (2026-10-03)

A new context reads the batch and writes the quiz; without sub-agents, the builder writes it and says so. _Rejected:_
a mandatory fresh reviewer (blocks agents without sub-agents); a cast of personas in one context (role-play).

## 16. No phase-id check (2026-10-03)

"The order of the work lives only in the roadmap" stays a rule in `AGENTS.md`. _Rejected:_ grepping phase ids outside
the roadmap (the pattern differs per project and would need a setting).

## 17. A lazy agent writing human-shaped code (2026-10-03)

The agent saves effort and tokens, never thought, and tells the human what it skipped. Lists follow their natural
series (the pilot's word lists had gaps and strays found one by one in the data). Coverage follows Pareto too.
_Rejected:_ fitting lists to the data alone; a coverage target.

## 18. The kit runs its own harness (2026-10-04)

`sdd/bin/sdd` runs the template's script, and one contract, `checks`, governs the script, its CI step and its tests.
Every batch on the kit goes through drift, size and the quiz, and the owner reviews it before each commit. GitHub
reads workflows only from `.github/workflows`, so the kit's audit job repeats the template's. _Rejected:_ a copy of
the script (two sources to keep in step); a symlink (a text file on Windows by default, as in decision 13); no harness
on the kit (the commit adding the script broke the size rule unnoticed).

## 19. Incentives, not locks (2026-10-04)

Every check can be bypassed: the harness helps an honest team see drift, size and understanding, it does not police
it. _Rejected:_ CI running the base branch's script, so that a batch cannot loosen its own checks.

## 20. Work in several batches (2026-10-07)

Work that takes more than one batch is planned in `sdd/changes/<slug>.md`: its why, then one section per batch with
the criteria it makes true. A fresh reviewer checks the plan and the human validates it. Each batch moves its criteria
into its module's contract and deletes its section, so the file holds only what is left; empty, it goes with its line
in `sdd/roadmap.md`, which only orders the work. Then a fresh reviewer reads each touched module whole, for a refactor
batch when it pays. A criterion is a plain sentence linked to the tests that prove it, and a link to a missing test or
file is drift. _Rejected:_ the whole plan in `roadmap.md` (it grows with the history and is read at every session);
checkboxes (stored status); planned criteria inside contracts (a contract that is not true yet); a When/Then template
(not how people write specs); a squad of personas (more tokens, no proven gain over one builder and a fresh reviewer).

## 21. The source is recorded at deploy (2026-10-09)

The deploying agent fetches the kit from the URL the human gives, GitHub by default, and writes it with the tag on the
first line of `sdd/README.md`; upgrade reads it back. A team behind an internal forge mirrors the repo, tags included.
_Rejected:_ a fork for the internal forge (two sources to keep in step); the GitHub URL hard-coded in deploy and
upgrade (unreachable or unwanted from some networks).

## 22. A token ledger by module, not by person (2026-10-25)

What agents spend is summed by module and month in the git notes `sdd-ledger`: each batch under a random key, written
by `sdd-fabrik` on the first of the month, so that no note leads to a commit, its author or its day. A batch changes
one module (decision 9), so its cost goes there; a `Large-Batch` splits by changed lines. The details (sessions,
sub-agents, MCP, skills, models) stay on the dev's machine, in the cockpit (decision 25); the ledger only reads its
`usage`, whose output is the contract. _Rejected:_ a note per commit (its author names the person: watching people,
not the product), OpenTelemetry (a collector to run), prices (they change, tokens compare).

## 23. Spend tokens where they pay (2026-10-25)

The cockpit measured the harness on real logs: a sub-agent starts at 35 to 39k tokens before reading anything, a
reviewer on Opus took 38% of the second pilot's cost, one of them 305 calls long, and `Bash` output 10%. So the
reviewer gets a smaller model than the writer's unless the batch is large or touches security or data; after a fix,
the same reviewer checks its quiz again (1 to 4k tokens in this kit; a fresh one costs about 50k, most of it its fixed
start); each batch starts in a fresh session; tests and builds print little when green. The core stays git and bash:
picking a model or resuming a sub-agent is a tool's feature, used where it exists and skipped where it does not.
_Rejected:_ a review pack that hands the reviewer its reading (the fixed start dominates, it would save little); a
terse "caveman" style for the agents (it cuts output, about 8% of the cost against about 50% for cache reads, and
blurs the quiz and the handoff, the text a human must understand).

## 24. install-hook writes the ledger's hooks (2026-10-25)

Each clone gets the `post-commit` and `pre-push` hooks with the `commit-msg` one, so that the ledger misses no
batch: without Python, `record` stops at once and `sync` has nothing to send. Each line passes in a
repo or a branch without the script, so a shared `core.hooksPath` takes them too. _Rejected:_ hook lines each dev adds
by hand (forgotten in some clones, so the ledger misses batches); an `install-hook --ledger` option (one more choice
per clone, for no saving).

## 25. The cockpit ships with the harness (2026-10-25)

`sdd/bin/cockpit` lands in each project with the other scripts. The ledger counts every dev, unless they set
`git config sdd.ledger false`, and an agent can read the dev's costs with nothing to install. A new tool still costs
agents nothing: an upgrade replaces the scripts without reading their diff. _Rejected:_ a tool each dev installs on
their PATH (most would not, the kit read as two products, and agents could not count on it); a ledger each dev joins
by choice (it names no one, and a tower that misses most batches tells nothing).

## 26. Superseded by 40.

## 27. The workflow keeps the loop, guides keep the rest (2026-10-25)

Every session reads `AGENTS.md` and `sdd/WORKFLOW.md`. The workflow keeps what each batch needs (COMPILE, the quiz,
contracts, decisions, trailers); the cases met once in a while (the first batch, a plan, the tokens, upgrade and
uninstall) move to `sdd/guide/`, linked from its top. What a session reads drops from 13.5k characters to 9.9k. The
kit block of `AGENTS.md` lists in three lines what the harness gives an agent, so that it finds the tools without the
dev. _Rejected:_ Agent Skills (each tool keeps them in its own folder, and their listing is sent with every session,
as an `AGENTS.md` line is); a `sdd help` command (a call to learn what a line can say).

## 28. The agent puts the cockpit's hints to the dev (2026-10-25)

At each handoff, the agent runs `bash sdd/bin/cockpit hints` and asks the dev about each line, with the change it
would make. A hint names a cost the logs show and what it buys: on this kit's logs of a week, seven MCP servers whose
instructions cost 95k tokens and whose tools were never called, a skill listing at 5% of the cost, 95% of it from
plugins never called here, Bash results at 10%, a context of 238k. Hints look at the dev's last 10 agent batches, and
one shown waits 10 batches before it comes back, so that most handoffs read an empty line. _Rejected:_ the agent
changing the setup on its own (MCP servers and plugins are the dev's, often for other repos); a hint at every batch
(the dev stops reading them); a window in days (a week is 30 batches for one dev and 2 for another); hints judged on
quality (the logs show what is used, not what it is worth).

## 29. A wrong quiz answer gets a hint and a way to say why (2026-10-26)

The quiz learns from the dev instead of only grading them. Under a wrong question, the hook writes in `QUIZ.md` the
key's hint and optional boxes: not understood, question unclear, the code does not do what I wanted. A wrong answer
often shows a gap of intent, not of the dev: the owner, answering from what they had asked for, found an implementation
that was not what he wanted. The block invites the dev to type *quiz feedback* to the agent, and is written once:
a new try leaves it as the dev left it, and counts nothing.
Nothing there blocks or allows a commit: the human keeps the last word. The terminal shows one line per wrong question,
the hint stays in the file next to its question. Hints point where to look and never name the box.
_Rejected:_ the quiz in the chat with the agent (tokens on every batch, the agent becomes the judge, tied to one
tool); new questions after a failure (one more round trip, nobody knows what to do next); the error rate as a measure
of what a dev knows (it measures the module and the question as much as the dev); intent questions inside the quiz
(they belong before and during the build).

## 30. The quiz journal stays on the dev's machine (2026-10-27)

The quiz journal keeps, on the dev's machine, what the dev ticked and wrote about the questions (what it keeps:
decision 37). It lives in the common git dir, so a dev working several batches in worktrees has one
journal, and it is never pushed, nor is anything taken from it (decision 36). The cockpit reads it for its hints, and
the agent reads it when the dev types *quiz feedback*: a keyword in `AGENTS.md`, so any tool that reads the file
answers it, and the agent spends nothing until the dev asks.
_Rejected:_ the merge request as the channel for feedback (it names its author); sending the agent the feedback at each
failure (tokens on every wrong answer, and the dev did not ask); a slash command (tied to one tool); a global switch for
learning (the journal stays local, the ledger already has `sdd.ledger false`).

## 31. The quiz follows the risk (2026-10-27)

The quiz weighs what a mistake costs. A contract may declare `risk: high`: the handoff and `audit` recommend a second
human's reading of a batch changing that module, whose quiz decision 39 sets. A batch of prose outside the contracts and
what modules govern (since 38) asks none: the human reads its diff, and a quiz on prose teaches little. Everything else
asks three, as before. The OWF notes (October 2026) ask for a demanding quiz and two humans on API contracts, security
and data; the owner kept the second human a recommendation, so that a dev alone can use the whole harness.
_Rejected:_ a required `Reviewed-by:` trailer at high risk (a dev alone could not commit); levels the dev declares for
themself (the risk belongs to the module, not to the person); a level guessed from the code (a rule the human cannot
read in the contract); a quiz on every Markdown change (questions on prose ask little).

## 32. Superseded by 36.

## 33. A dev new to a module is spotted from git, never from the quiz (2026-10-27)

`sdd brief <module>` tells a dev's first batch in a module from the history alone: no commit of theirs in its contract
or governed paths. The agent then offers a discovery mode, applied only on a yes, and names the devs who delivered
there most so the dev knows whom to ask. Seniority is never guessed: a senior new to a module is new to it, and a
junior who built it is not.
_Rejected:_ a junior or senior profile (the agent would judge the person); the quiz results to adapt the help (decision
29: they measure the module and the question as much as the dev); discovery mode applied without asking (the human
keeps the hand).

## 34. Name to coordinate, never to measure (2026-10-27)

`sdd brief` tells the dev what waits before they produce more: a quiz in another of their worktrees, then the remote
branches not merged after `REVIEW_WAIT_HOURS`, oldest first, each with its author's name so the dev knows whom to
see. The rope team moves at the pace of what it reviews, not of what its agents produce: one dev with several agents
and two devs reading each other meet the same line. It reads only what git already shows everyone, and never fetches.
_Rejected:_ a count of branches or waiting hours per dev (it would measure people, decision 32); a fetch at each brief
(slow, and a network call the dev did not ask for); a block until the reviews are done (the human keeps the hand, and
a dev alone has no one to wait for).

## 35. A harness that proposes its own rules (2026-10-27)

`cockpit hints` reads the quiz journal on the dev's machine: when, over their last 10 batches, a module's answers were
flagged unclear or not what they wanted twice or more, it says so, and the agent proposes the rule it would write (in
the contract, the coding style or the quiz instructions). The dev decides, and the rule comes in a batch of its own.
The harness learns from the people who use it without anyone's answers leaving their machine: only the rule does.
_Rejected:_ writing the rule without asking (the human keeps the hand); the team's quiz lines (the dev's own flags are
what they can act on, and the quiz never leaves a machine, decision 36); one flag (a single unclear question is noise,
two point at something).

## 36. The quiz stays home (2026-10-28)

Nothing the quiz learns about a dev leaves their machine: the token ledger notes tokens only, `ledger report` loses
its quiz tables and `ledger quiz` goes. Decision 32 pushed each question's title, tries and causes without a name, but a
title names its batch, and `git log` names its author: the review after the rope team found who had not understood
what, in the kit's own ledger. Even when anonymity holds, what counts is what the dev believes: one who thinks they are
read from above stops ticking "not understood", and the quiz stops being an honest moment between the dev and the
code. The `q1` lines already pushed stay: they are the owner's own quizzes on the kit, and removing them means
rewriting shared notes. The team learns from a quiz badly asked through the rule its dev proposes (decision 35).
_Rejected:_ lighter quiz lines (first try or not, unclear and not wanted only: still a measure of people that a title
or a month can point back to); a count of devs per module who passed a quiz (it counts understanding, and `git log`
already shows who worked where); rewriting the pushed notes (the kit's ledger holds only its owner's quizzes).

## 37. The journal keeps the flags, at the pass (2026-10-28)

The quiz journal gets a line only for a question the dev flagged or commented, and only when the quiz passes, when the
boxes are their last word: the time, the batch's modules, the causes, the title and the words. Its one reader, the
cockpit, needs no more. The tries, the batch fingerprint and the questions nobody flagged had a reader, the ledger,
which decision 36 removed. The post-commit hook journals it once the commit exists, so a later hook that fails journals
nothing; an amend with a new quiz journals that one too, and the cockpit counts a flag once per module, title and cause.
*quiz feedback* reads `QUIZ.md`, which holds the same, under each wrong question.
_Rejected:_ a line at every try (counted twice, read by no one); the journal in the ledger's place for a report on
the dev's own understanding (a score of themselves nobody asked for).

## 38. Markdown a module governs asks a quiz (2026-11-02)

Decision 31 spared prose outside the contracts, which the script read as any Markdown outside `sdd/modules/`. A module
may govern Markdown that carries its intent, such as templates or docs it ships: a batch there now asks a quiz like
the module's code. A batch that deletes a `risk: high` contract is judged at high risk, as one that drops the line
already was. Both were found by the review of the rope team's scripts.
_Rejected:_ sparing every Markdown file, as before (prose a module governs is its behavior); reading risk from the
staged tree only (the batch that removes a high-risk module is one to read twice).

## 39. The quiz covers the batch (2026-11-02)

Five questions said nothing of what they left out: a quiz on one function of a seven-hunk batch passed as well as one
on all of it. Each `See` line now cites one to three places, and the trailer says how many hunks of code they meet,
`Quiz: 3/3, covers 5/7`: a fact about the code, in each commit, with no aggregate, as decision 36 asks. A new file is
one hunk; a deletion is met at the line before or after it. At high risk the quiz has three questions or more and
`audit` fails until they cite every hunk; the hook never checks it, so the human is never refused for the reviewer's
miss. This supersedes the five questions of 31.
_Rejected:_ five questions (a count, not a reach); coverage on the hook (it would refuse the human for the reviewer's
quiz); a share of lines (a long new file would weigh more than the risky line beside it); questions on the technology
(they test the reader, not their grasp of this code).

## 40. The harness moves to Python 3 (2026-11-02)

The scripts grew to 825 lines of bash with awk programs inside quotes, plus 331 of Python, which the owner and the team
find hard to read, and the readers of agent logs (Claude Code, opencode, then Kilo Code and Copilot) parse JSON, which
awk does badly: the bash and Python readers of Claude Code's logs already disagree on an escaped quote. The owner
confirmed that Python 3 is on every dev machine of the team. The scripts move to Python 3, standard library only, behind
the same commands, so that the tests, which call the commands, prove the move. Decision 3 rejected Python as a runtime
to install and too heavy to copy; the team has the runtime, and the standard library keeps the copy to a few files with
no package to install. This supersedes decisions 3 (bash and git only) and 26 (the ledger's reader without Python). The
move comes after the fixes the team needs to test the harness (`sdd/changes/team-ready.md`).
_Rejected:_ bash with its awk in `.awk` files (readable in part, JSON still hard); a compiled binary (a build and a
release per platform); one big batch for fixes and move together (nobody could read it, against the harness's own
rule); the pre-commit framework (it needs pip).

## 41. The pushed ledger has no history (2026-11-03)

Each `record` was a notes commit and `sync` merged the clones' chains, so `git log --graph refs/notes/sdd-ledger`
showed each clone's notes on its own side of a merge, in commit order: matched with the agent commits of an author,
the k-th note gave each dev's cost per batch (review of 2026-11-02), against decision 22. `sync` now pushes the merged
notes as one commit with no parent, dated the first of the month by `sdd-fabrik`; the local chain is never pushed.
A lease on the fetched commit keeps a ledger pushed meanwhile from being overwritten: it is merged at the next push.
_Rejected:_ one ref per dev (it names them); squashing the local chain too (the local history names no one else).

## 42. Superseded by 43.

## 43. The quiz speaks the human's language, its block too (2026-11-03)

The owner talks to the agent in French and asked for everything the quiz shows in French, the block under a wrong
answer included: a question read in a second language tests the language as much as the code. The writer tells the
reviewer the language the human writes in. The reviewer writes the quiz in it, and, for a language other than
English, eight lines after the key's answers that word the hook's block. The journal reads the block's boxes by their
place, so it reads the same in every language. The marks the hook parses (`## `, `See`, `- [ ]`) and its messages in
the terminal stay in English, like git's own.
_Rejected:_ a language setting in the repo (a team may mix languages; the human's own words are the evidence);
translations shipped in the script (one table per language to maintain); the terminal messages translated too (the
same eight lines would not cover them, for lines read once).

## 44. Python is a firm dependency (2026-11-04)

Since the move to Python (decision 40), no check runs without it. Without Python 3.10 or later, `install-hook` fails
and says what to install, and the commit-msg hook refuses with the same words: a batch never goes in unchecked without
anyone seeing it, and `--no-verify` still passes, as for any check (decision 19). The post-commit hook, the ledger and
the hints say nothing, and never stop a commit or a push. Each command is a `sh` launcher of a few lines that tries
`python3`, `python` and `py -3` and checks the version, which also skips the stub Windows answers `python3` with until
Python is installed. 3.10 is the floor the CI pins; Ubuntu 22.04 LTS ships it. The code runs on 3.9 too (the three
suites pass under 3.9.25), but 3.9 is no longer maintained since October 2025, so a Mac whose only `python3` is
Apple's (3.9 with the Command Line Tools) needs a newer one, from python.org or Homebrew.
_Rejected:_ the hook passing silently without Python (an agent batch would go in unchecked); a Python found once at
install and written into the hooks (a dev who installs Python later would have to run `install-hook` again); bash
kept for the checks with Python for the rest (two languages to read, and the awk decision 40 left).

## 45. Only a tool's reader knows the tool (2026-11-04)

The cockpit's report and hints were written for Claude Code: they named it, took its price ratios and its log walk
from its reader, and matched MCP servers to tools by its `mcp__<server>__<tool>` names, through labels whose prefixes
they parsed back. Now a reader that can weigh its calls has `NAME`, `PRICES` and `calls`, which yields each reply as a
`Call` and fills a `Sent`: the cost of each source sent along, a kind and a name, and which MCP servers and plugins were
called. Both live in `fabrik/logs/__init__.py`. The cockpit only sums calls and reads `Sent`, for every reader that
has `calls`, so that Kilo Code or Copilot is a module in `fabrik/logs/` and nothing else.
_Rejected:_ a base class for readers (two readers, one with `calls`: a module with three names says as much); the
reader computing the whole report (each tool would write its own hints, worded differently); keeping one tool in the
cockpit until a second can weigh its calls (the next one would have to untangle it first).

## 46. A defensive finding shows its input (2026-11-04)

A finding of the fresh reviewer that adds a check, an error path or a fallback names an input the code really
receives and gets wrong; without one, the writer leaves it out and lists it in the handoff. The coding style already
refuses code "just in case", but nothing asked the same of the findings, which the writer fixes as they come. No pilot
counted such findings; the evidence is Anthropic's write-up on Scion (October 2026), whose engineers had to turn down
an over-defensive adversarial review that added complexity.
_Rejected:_ a reviewer told to skip such findings (a gap at a real boundary is one to fix); the rule in the coding
style alone (it is there already, and the findings are fixed in step 6, not against the style).

## 47. Superseded by 55.

## 48. Git's own files ask no quiz, like Markdown (2026-11-05)

A batch whose changed files are all Markdown, `.gitignore`, `.gitattributes` or `.gitkeep`, outside every module and
contract, asks no quiz, and those git files count neither in the size nor in the hunks a quiz covers. In the first
field use (opencode and Qwen, 2026-11-05), the GENESIS batch wrote the project's documents and a `.gitignore`; the
reviewer wrote no quiz, as the human expected, and the hook refused the commit. The human took the `.gitignore` out to
the next batch. These files change what git tracks, not what the product does, and the human reads them in the diff.
_Rejected:_ every dotfile (`.github/workflows/`, `.eslintrc` and `.env.example` carry behavior); a level judged on
"no hunk of code" as the coverage counts it (a lock file alone would ask nothing, and a dependency bump deserves a
question); a list the project sets (one more setting, for three files nobody debates). Decision 56 asks a quiz of
the files a `sensitive` list matches.

## 49. The human skips a quiz with a reason (2026-11-05)

`Bypass-Quiz: <reason>` in the message lets a commit pass the hook without a quiz; drift and size still apply, the
reason is required, and the trailer stays in the history. The owner asked for it: a dev with a good reason (a batch
redone after a passed quiz, an urgent fix) should not have to hide it. Today they can drop `Agent-Assisted` or use
`--no-verify`, and nothing says why.
_Rejected:_ a reason that is optional (the trace is the point); a bypass that also lifts drift and size
(`Large-Batch` and `Spec-Unchanged` already say what they lift); refusing it on a `risk: high` module (the human owns
the commit, the trailer shows the choice).

## 50. The script leads a batch, not the prose (2026-11-05)

`sdd next` reads the batch's state in git (contract, staging, message, audit, quiz) and prints the one step left, with
its number in COMPILE. A light model on Kilo Code (2026-11-05) dropped steps 4 to 7 after some 60 tool calls; the next
one may drop others. Whatever step was skipped, the state shows it, and one rule in `AGENTS.md` replaces remembering
seven steps. Strong and light models get the same guidance.
_Rejected:_ a reminder of the last steps in `AGENTS.md` (covers the steps it names, not the next one skipped);
guidance by model (a catalogue goes stale in a month, and no tool says how able its model is); a reviewer agent
written for each tool at setup (a model that skips the audit skips the reviewer too).

## 51. A module sets its own batch size, higher or lower (2026-11-06)

A contract's `batch-lines` replaces the repo's for a batch that changes that module's code, and a SIZE line names the
file that sets the limit, so that a dev sees it comes from their module and not from the repo. The plan of 3.2 had a
module only lower it; the owner asked for both ways, seeing no reason to forbid more lines where a module needs them.
A batch that changes a `batch-lines`, in a contract or in `sdd/config.yml`, is judged on its new value at once, and
gets `NOTE <file>: batch-lines goes from <old> to <new> in this batch.`, so that the human sees an agent giving itself
room, as they see a `Large-Batch` trailer. The owner flagged the first version in the quiz ("not what I wanted"): a
module that needs more lines had to commit its contract first, with a quiz of its own.
_Rejected:_ a module that only lowers the repo's limit (a module of generated code or migrations would need
`Large-Batch` at every batch); judging a batch on the smaller of its parent's value and its own (one more commit and
quiz to raise a limit, for a guard no stronger than the note); a new value without a note (nothing would show an agent
raising it); the limit applied to each module's own lines in a batch of several (such a batch needs
`Large-Batch` already).

## 52. The repo's settings live in sdd/config.yml (2026-11-06)

The kit ships `sdd/config.yml` with its defaults as comments, and an upgrade never replaces it; it holds the repo's
`batch-lines` and `risk` as flat `key: value` lines, the format of a contract's front matter, and a contract sets the
same keys for its module. GENESIS and ADOPT ask the batch size and the risk and write only what differs; a contract
does the same against the repo. Teams starting with Kilo Code and Copilot asked to set both at setup, and the only way
was to edit `size.py` or every contract, which an upgrade replaces or forgets.
_Rejected:_ real YAML (a parser outside the standard library, for two keys); settings in `AGENTS.md` (the agent reads
them, the script does not); `git config` (one clone's, not the repo's, and never reviewed in a diff); keeping
`MAX_LINES` in `size.py` as the project's knob (an upgrade replaces the file).

## 53. One to three questions below high risk (2026-11-06)

Below high risk a quiz has one to three questions, as many as what the batch changes calls for; high risk keeps three
or more, each citing every hunk of code. Three questions on a one-line fix taught nothing the first did not (asked by
the owner on 2026-11-05). What the quiz must reach is the module's risk's business, not a count: the trailer already
says how many hunks the questions cite. The note on a right answer always in the same place needs two questions.
_Rejected:_ fewer than three questions only when they cite every hunk (a rule of reach on every module, which is what
`risk: high` is for); one question for a batch without a hunk of code (the reviewer judges what a contract change
calls for).

## 54. Code outside every module takes the repo's risk (2026-11-06)

A batch is judged at the highest risk of the modules it changes, and code that no module governs counts at the risk of
`sdd/config.yml`; Markdown and git's own files outside every module still ask no quiz (decision 48). A repo set to
`risk: low` says it wants no quiz on code, and its scripts, build and CI files at the root are code of the repo like
any other; one set to `high` says a mistake costs much anywhere. The batch that lowers a risk is judged at the risk it
had, as one dropping `risk: high` already was.
_Rejected:_ code outside every module always at `normal` (a repo at `low` would still be quizzed on its root files,
which are most of a young project); always at `low` (unowned code at a `high` repo would pass with no quiz, the
opposite of what the setting says); a risk of its own for code outside every module (one more key, for what a
contract governing those files already sets).

## 55. Superseded by 77.

## 56. A sensitive file asks a quiz at any risk (2026-11-06)

Some files steer the project or the harness whatever their module's risk: the workflow, the script, the guides,
`sdd/config.yml`, `AGENTS.md`, `CLAUDE.md`, the architecture, the coding style, the product and the contracts. A
batch that changes or deletes one is judged at `normal` at least, so a repo at `low` or `intent` still reads what it
hands the agents; this supersedes 48 for those files, Markdown or not. The kit's list holds until `sdd/config.yml` sets `sensitive`,
which replaces it, and a contract's list adds to the repo's, so a module at `low` keeps its schema under a quiz. Both
lists are read in the parent and in the batch, so the batch that empties a list is judged by the old one. An entry is
a path, a folder ending with `/` or a regular expression between slashes, never split, so a path may hold a comma.
_Rejected:_ git pathspecs as in `governs` (a glob cannot say "any `.sql`, at any depth" as plainly, and `:!` reads
badly in a list meant to grow); a list in brackets (`[a, b]` splits a path with a comma; it stops the commit and shows
the `- ` form instead); a contract's list for its own files only (a module that cares about a file outside it would
have to govern it); `high` for a sensitive file (three or more questions on a one-line fix of the workflow).

## 57. Superseded by 77.

## 58. The kit's sensitive list holds what steers the agents (2026-11-06)

The kit's list adds the CI workflows (`.github/workflows/`, which replay drift and size), `.claude/` and the files
where the deploy denies `git commit` (`opencode.json`, `kilo.jsonc`, `.vscode/settings.json`), and it reads `AGENTS.md`
and `CLAUDE.md` at any depth and in any case, as one expression, since Codex and Claude Code read nested ones and a
case-insensitive disk reads `claude.md`. An agent batch at `low` could otherwise lift the deny rules, change what
steers the next agents or turn off the CI check, with no question asked (security review of affbcb0, 2026-11-06).
The list stays one a project replaces in `sdd/config.yml` (56): it grows from ten entries to fourteen.
_Rejected:_ `.github/` whole (issue templates and dependabot would ask a quiz for nothing that steers an agent); every
tool's rules folder (`.cursor/`, `.github/copilot-instructions.md`, `GEMINI.md`: a catalogue that goes stale, for tools
that also read `AGENTS.md`); `.gitlab-ci.yml` now (it comes with the GitLab CI of 3.3).

## 59. The kit ships a GitLab CI job (2026-11-06)

The template carries `.gitlab-ci.yml` beside the GitHub workflow, and the deploy copies the one of the repo's forge,
read from its remote or asked of the human. Teams on GitLab replayed drift and size only by hand, and the first team to
pilot the kit works on GitLab (2026-11-04). The job runs in branch pipelines, where jobs without rules run, from
`CI_COMMIT_BEFORE_SHA`; a new branch's base is zeros, so it audits the commits the default branch lacks. It takes the
`python:3.12` image, which has git and bash, and leaves the `workflow:` and `stages:` of the file it joins alone. A
project whose jobs run in merge request pipelines gives it their rules: the base is zeros there too. "CI for other
forges" leaves the contract's non-goals for "forges other than GitHub and GitLab". The control at the merge request,
on the roadmap, will need merge request pipelines for every job of the project that chooses it: a setting of the
project then, not a default of this job. The kit's `sensitive` list holds `.gitlab-ci.yml` beside
`.github/workflows/`, for the reason of decision 58: a batch at `low` could otherwise turn the CI check off with no
question asked.
_Rejected:_ merge request pipelines from `CI_MERGE_REQUEST_DIFF_BASE_SHA`, as planned (a job that asks for one makes
GitLab create a pipeline holding that job alone, since jobs without rules never run there; it becomes the merge
request's pipeline, and "Pipelines must succeed" stops waiting for the project's tests: fresh review of this batch);
the tip alone for a new branch (a first push of five commits would replay one); a `workflow: rules` block (it changes
every job of a project's pipeline); a file to `include:` (one more file for a dozen lines; a remote include of the kit
runs whatever its main holds); a slim or Alpine image (no git, and an install step that runners behind a proxy fail);
both CI files in every repo (a workflow that never runs looks like a check); every forge (no team asked, and they run
the same command).

## 60. Superseded by 77.

## 61. A quiz written for the batch marks it as an agent's (2026-11-07)

The hook told an agent batch only by `Agent-Assisted: yes` or an agent's co-author address, both in a message the human
may retype: a dev committing from the IDE's message box sent an agent batch in as their own, with no quiz and two
warnings, and nothing said so (review of 2026-11-07). A quiz key whose first line is the fingerprint of the staged batch
is a reviewer's proof that the batch was quizzed: the hook treats it as an agent batch and adds `Agent-Assisted: yes`
to the message, so that CI, the ledger and the history count it too. A key written for an earlier state of the batch
marks nothing, as the fingerprint already says.
_Rejected:_ asking for `QUIZ.md` as well (deleting it would skip the quiz again, silently); refusing a commit without
the trailer when a key exists (the human would have to retype what the hook can write); a trailer added by `sdd next`
or the agent (the message the human commits is not the one the agent wrote).

## 62. Brief leaves out abandoned branches and bots' (2026-11-07)

`brief` showed the three oldest remote branches not merged, so in a repo that keeps abandoned branches it printed the
same ones forever: with four branches of 2025 and one pushed five hours ago, it gave three of 600 days or more and never
the fresh one (review of 2026-11-07). A branch whose last commit is 14 days old or more (`abandoned-days` in
`sdd/config.yml`, decision 63) no longer waits, and neither does a bot's (a name ending in `[bot]` or holding the word
bot), whose updates wait for no one in particular. The order of 34 stays: the oldest review still waiting comes first.
Each branch out of the window costs no `git log`.
_Rejected:_ newest first (the review that has waited longest is the one to finish, decision 34); a fetch to see which
branches were deleted on the remote (34 never fetches); a list of bot names (each forge and tool names its own).

## 63. Every setting of a project lives in sdd/config.yml (2026-11-07)

The owner asked for every setting a project may change in `sdd/config.yml`, each named plainly, rather than in
constants of kit files that an upgrade replaces and that the upgrade guide asked an agent to keep by hand (against
52). `brief` reads `review-wait-hours` and `abandoned-days` there first, as whole numbers, with the kit's defaults shown
as comments in the file; `NOT_CODE` and `AGENT_EMAILS` follow in batches of their own. What stays in the code is what a
project does not tune: the kit's rules (the quiz's form, the risk levels), the facts of a tool (a provider's price
ratios, the shape of its logs) and the names of the harness's own files.
_Rejected:_ `sdd/config.yaml` (deployed repos already hold `sdd/config.yml`); settings in `git config` (one clone's,
never reviewed, as 52 says); one batch moving them all (several modules, beyond the size the harness asks of agents).

## 64. agent-emails and not-code are lists of the config (2026-11-07)

The two settings the upgrade guide still had an agent keep by hand in kit files, `AGENT_EMAILS` (`git.py`) and
`NOT_CODE` (`size.py`), become `agent-emails` and `not-code` in `sdd/config.yml` (decision 63). Both are written as
`sensitive` is, one entry per `- ` line, read by the same function, and each replaces the kit's list when set, the
kit's shown in the file as comments. `agent-emails` holds plain addresses, matched without case. `not-code` holds
paths, folders and expressions, lock files by default; Markdown and git's own files stay outside the code whatever it
says, since 48 rejected a list for them. A batch that changes either is judged by the stricter of its parent's list and
its own: one that drops an address is still an agent's, one that widens `not-code` still counts the lines it would
hide. The ledger and the cockpit count agent commits with the addresses at HEAD. Both come in one `Large-Batch`, not
the batches 63 announced: they share their reader in `contracts.py`, so each alone would span several modules
anyway.
_Rejected:_ the addresses as one regular expression, as the constant was (an address with a `+` or a `.` would need
escaping); the batch's own list only (an agent could hide its lines or its mark in the commit that does it); the list
adding to the kit's (a project could not stop counting an address that is a human's, such as a shared noreply).

## 65. The quiz follows what the batch changes, not who answers (2026-11-08)

A dev's batch is not only code: it may move a contract, a module's boundaries, its tests or a decision, and the dev who
commits it must show they understood that part, not only the lines. The roadmap had a quiz per role, the roles and
their fallbacks in `sdd/config.yml`, and a choice of checkpoint between commit and merge request: roles times quiz
types times checkpoints, each pair to document, test and replay in CI, and a harness that must know who is who, against
"a dev alone uses the whole harness" and "name to coordinate, never to measure" (spec of 2026-10-26). The quiz keeps
one checkpoint, the commit, and one person, the dev who commits. Two axes split what the level mixed: the risk says
how many questions, what the batch changes says what they are about (behavior, promise, structure, proof, rejected
option), each still citing the batch. The reviewer picks that by reading the diff, in the workflow's prose, not in a
rule of the script. A second human stays a recommendation with a name, as at `high` today. A merge request gets a
summary of its commits' trailers in CI, never a second quiz.
_Rejected:_ a quiz per role and the roles in the config (above); a cursor between commit and merge request (two full
modes to keep, and a quiz at the merge request is what others already offer); the PO's functional level outside git,
and run, UX and QA as levels of their own (a tool beside the repo, and question kinds cover what they would ask).

## 66. The quiz's answers stay with the reviewer until the commit (2026-11-08)

On `9852c39` the quiz proved nothing: Kilo's reviewer gave the writer each right answer in its report, the writer
printed the key while checking the state, and an agent that fixed the quiz listed its letters and why in the handoff.
Nothing forbade it. The reviewer now reports how many questions it wrote and what the audit printed, the handoff says
how many questions the quiz has, a house rule in `AGENTS.md` keeps every right box and its reason out of what reaches
the human before the commit, and only the agent that writes the quiz opens the key (the reviewer, or the writer of a
tool that cannot spawn one). *Quiz feedback* talks the questions through as the hint does: where to look, never which
box or why it is right.
_Rejected:_ hiding the key from the agents (the reviewer writes it and the hook reads it from the same clone, so any
agent there can read it too); a check that greps the handoff for letters (the handoff is not in git, and a reason
gives the answer away as well as a letter).

## 67. The size counts no blank line (2026-11-08)

`batch-lines` is there so that a human can take in what they must understand, and a blank line holds nothing to
understand: a file of 211 lines of code spaced by blank lines counted 633 lines, three times the limit. `size.py` now
reads the patch with `-U0` and counts the lines it adds or deletes that hold something other than whitespace, binary
or not; prose renamed to code counts its lines that are not blank.
_Rejected:_ `--ignore-blank-lines` (it drops only hunks whose lines are all blank, a hunk mixing code and blank lines
still counts them); counting comments out too (a comment is read, and telling one from code takes a parser per
language).

## 68. A quiz left behind is found among the commits made since its key (2026-11-08)

On 2026-11-04 the quiz of 12558ff stayed in `QUIZ.md` after a pull: the clone's shared `post-commit` predates the line
that calls `committed`, and its fallback only matched the key against HEAD's tree on `HEAD^` or `HEAD@{1}`, so a merge
on top hid the batch for good and its flagged questions never reached the journal. `committed` now reads, in one
`git log --since`, the commits made since the key was written, and matches each one's own tree and first parent. The
fingerprint is worked out in Python as the same hash `git hash-object` gave, so keys already written still match and
a pull of 200 commits costs no 200 processes. A pull with rebase rewrites the batch's parent: its quiz still stays.
_Rejected:_ the last N commits (a pull brings others' newer commits first, so any N can miss the batch); only the
commits that carry `Quiz:` (a batch committed with `--no-verify` must leave no quiz either); telling the dev the
hooks are out of date (a batch of its own, and the quiz would stay until they act).

## 69. A quiz replaced before any commit is journaled by the next fingerprint (2026-11-08)

On 2026-11-05 a demo repo took a decision from a quiz answer flagged "the code does not do what I wanted", yet its
journal was empty: the journal read only the quiz of the commit that passed, and a batch redone after a flag gets a new
quiz first. The reviewer runs `fingerprint` before writing one, so `fingerprint` now journals the flags of a quiz left
for a batch that changed since and was never committed, on the modules staged now, once per state of `QUIZ.md`. The
lines keep format v2 and no mark: `not-wanted` already says why the batch was redone. The cause is a guess, not
checked: the demo's opencode sessions are not on this machine.
_Rejected:_ a `reworked` mark in a v3 line (a new format and two readers in the cockpit, for a reason the box already
gives); journaling at each failed commit (the boxes are ticked after the hook writes the block, so the dev's last word
comes later).

## 70. `sdd doctor` says what is out of date, and the kit carries its version (2026-11-08)

The two bugs of the first field use came from a clone, not from the kit: a shared `post-commit` that predates the
`committed` line, found by reading the hooks by hand. `doctor` prints in one paste what a bug report needs: the kit's
version, Python, git and the OS, the hooks folder, the ledger on or off, the replies each log reader found in 30 days
and an audit's time. A NOTE names what to fix, and a hook counts as up to date when it runs each command of the kit's
line, so a line a hook manager rewrote still passes. `VERSION` in `fabrik/__init__.py` is raised by the human before
each tag; `doctor` compares it with the tag on the first line of `sdd/README.md` to catch an upgrade half done, and
a kit test fails when it is older than the last tag, so the test job fetches the tags.
_Rejected:_ the first line of `sdd/README.md` alone (nothing to raise, but a partial copy of the files goes unseen);
reading the version from the kit's git tags (a deployed repo has none); a doctor that fixes what it finds (the hooks
may be shared or built by a manager, and `install-hook` already writes what it may).

## 71. `next` names the hooks out of date (2026-11-08)

A hook out of date fails without a word: the quiz stays after its commit, or the ledger notes nothing, and on
2026-11-04 it took reading the hooks by hand to see it. `next`, which the agent runs again and again, now adds one line
naming the hooks that do not run a command of the kit, and sends to `doctor`, which says what to do with each.
_Rejected:_ the full list of what to add (it would repeat at each `next`, `doctor` gives it once); the line in `audit`
(CI runs it, where no hook runs); refusing the step (a check that locks, for a cause outside the batch).

## 72. The cockpit says when it no longer reads a log format (2026-11-08)

Claude Code changes its logs with each version, and a reader that stops finding replies or token counts gives figures
too low, or none, without a word. Measured on 221 logs of this machine (versions 2.1.292 to 2.1.319): 25 entry types
and 34 attachment types, of which the reader uses 6, new ones in each version; 6735 replies, none without a token
count. `report` and `hints` now say so when the logs with an entry in the window hold no reply the reader finds, or
when replies hold none of the token counts it knows, and send to `doctor` for a bug report. A log counts by its
entries, not its mtime: in four real windows the logs touched held no reply, all of them empty (14 files of 221 are
sessions closed before a prompt) or resumed without a prompt, with no entry dated in the window.
_Rejected:_ counting the entry types the reader does not know (most of them it has no use for, so it would fire on
every version); the logs' mtime (it gave those four false alarms); the same guard for opencode and Kilo Code (they
have no report yet, and `doctor` shows their replies read).

## 73. SDD-Fabrik becomes Cordee (2026-11-08)

"SDD" put the kit among the spec tools and "Fabrik" said to produce more, the opposite of its stance: agent code
enters history only as fast as a human understands it. A *cordée* is a rope team of climbers, who move at the pace of
the one who follows. `cordee` and `cordee-harness` are free on PyPI and npm (checked 2026-11-08), trademarks not
checked. The folder `sdd/` becomes `cordee/`, the command `cordee/bin/cordee`, the Python package `harness` (a package
named `cordee` would sit next to the launcher of the same name), and with them `.git/cordee/`,
`refs/notes/cordee-ledger`, `cordee.ledger`, the `# cordee` and `<!-- cordee -->` markers and the `cordee-audit` job.
Every repo running the kit belongs to its maintainer, so the kit reads no old name: `guide/from-sdd-fabrik.md` tells
an agent how to switch a repo, and the earlier decisions keep the names they were taken under.
_Rejected:_ a version that reads both names (code to keep for repos one person switches by hand); keeping
`sdd/bin/sdd` as the command (a name the kit drops, kept only to type less); `grasp`, `belay` (taken, see the notes
of 2026-11-08), `teachback`, `gotit` (free, but they name the quiz, not the pace).

## 74. The ledger syncs only what a remote has not seen (2026-11-08)

Each push fetched and pushed the ledger, even when the dev had no new note: one more round trip at every push, for
nothing to send. `sync` now keeps, per remote, the tree of the ledger it last took, in the clone's
`.git/cordee/ledger-synced`, and does nothing while ours is the same. The notes of others then reach a dev only with
their next own note, so a local `ledger report` can lag behind the remote's; `git fetch` of the ref catches it up.
_Rejected:_ `git ls-remote` before each push (still a round trip); one state for all remotes (a second remote would
never get the ledger); fetching anyway and pushing only on change (the fetch is the cost).

## 75. A test times `audit` with 40 contracts before any cache (2026-11-08)

`audit` reads each contract with its own `git show`, several times: 508 git calls, 252 of them `git show`, for one
staged batch in a repo of 40 contracts, 0.9 s on Linux. A process costs much more on Windows, where no one has timed
it. `test/run`, which CI runs on Linux, macOS and Windows, now fails when `audit` takes 3 s or more there; the cache of
`git show` by tree and path in `contracts.py` comes only if Windows goes over.
_Rejected:_ the cache now (code for a cost no one has seen); a timing job of its own in CI (a fourth suite to run
before each batch, for one test); the time printed without a limit (a number no one reads on a green run).

## 76. The reviewer asks about what the batch changes, from the lines it cites (2026-11-08)

Decision 65 split the quiz in two: the risk says how many questions, what the batch changes says what they are about.
The workflow still told the reviewer only how to ask about code. It now names a subject per kind of change: behavior
for code, the promise for a contract or `product.md`, the structure for `depends`, `governs` or `architecture.md`, what
a test pins and misses, the rejected option for a decision. Of the seven questions devs flagged in this repo's journal,
four set a scenario to run through the code ("if measure() stopped reading reader.calls() at the first Call, what
would the mcp hint say?"), all four ticked "not understood": a question is now answered from the lines its `See`
cites.
_Rejected:_ the subject as a rule of the script, by file type (a contract with code would need a pair of rules for each
mix, and the reviewer reads the diff anyway); dropping "what breaks if this line goes" (it reads one line, the trouble
was the chain across files); a question per kind of change in every batch (one to three questions, picked where the
batch weighs).

## 77. Three risks: none, normal, high (2026-11-08)

The risk now says only how many questions: none, one to three, or three or more citing every hunk; what they are about
comes from what the batch changes (65, 76). `intent` (55) asked a quiz only when a contract moved, and the step less
for a batch of tests alone (57, 60) took a level down by the links of the contracts left as they were: two rules that
set what the quiz is about through its number, with the linked and proven files `drift` gathered only for them, and a
security review was already needed to close a gap of the step (60). A contract that moves is now quizzed like code,
and a batch of tests alone at `normal` asks one to three questions on what the tests pin and miss. `low` becomes
`none`, the word for what it does. No repo used these levels, two days old, so the kit reads no old value.
_Rejected:_ keeping `low` (it names a risk, where the value says the quiz); `intent` beside the three (the reviewer
already asks about the promise when a contract moves); the step for tests on three levels (`normal` would step down to
`none`, no question on a test that may lock a bug in).

## 78. A deploy command does the copy and the upgrade, the agent the merges (2026-11-08)

The deploy had the agent copy `template/` file by file without overwriting, pick the CI file from the host of
`origin`, edit the first line of `cordee/README.md` and run `install-hook`: four steps a script does the same way each
time, and an agent may not. `bash <tmp>/template/cordee/bin/cordee deploy <source> <tag>` now does them from the
kit's clone, in Python like the rest, tested by `test/run`, and does the upgrade and the switch from SDD-Fabrik too:
it replaces the kit's own files (`cordee/bin/` and `cordee/guide/`, cleared first so deleted files go, and
`cordee/WORKFLOW.md`), replaces the marked block in `AGENTS.md` when the `cordee` or `sdd-fabrik` markers are already
there, and updates the `Deployed from` line of `cordee/README.md`. It lists the other files already in the repo; their
merges (or on upgrade, what `git diff <old> <new>` changed in them) and the deny rules, which depend on the tool the
agent runs in, stay with the agent. A host that names neither forge stops it before any write, and the human answers
through `--forge`.
_Rejected:_ a script at the kit's root, outside `template/` (nothing more in each repo, but a fourth thing to test,
that `upgrade` could never reuse); a second `upgrade` command (the same steps as `deploy` once the kit's files and
markers are replaced); the deny rules in the command (Claude Code and opencode as JSON, Kilo as JSONC, Copilot and the
others by hand: two paths for one step); appending the `AGENTS.md` block and the `@AGENTS.md` line on a first deploy
(a third of the merges, with the CI merges still to the agent); the forge from the whole URL (a GitLab repo named
`github-tools` would get the GitHub file).

## 79. The cockpit and the ledger are opted in through `tokens: true`, and deploy guides the setup (2026-11-08)

A repo that adopts Cordee for its contracts, size limit and quiz may want no token reading and no `pre-push` network
hook. `tokens` in `cordee/config.yml` is `false` by default: `install-hook` then writes only `commit-msg` and
`post-commit` (`committed`), removes a `pre-push` hook it wrote earlier, and `__main__.py` and `doctor.py` import
neither `cockpit`, `ledger` nor `logs`, so the core runs even when their files are removed. Setting `tokens: true` and
running `install-hook` adds `ledger record` to `post-commit`, writes `pre-push` (`ledger sync`), and has the workflow
run `cockpit hints` at handoff; every clone of the repo gets the same hooks from `cordee/config.yml`. During deploy,
the agent walks the human through that choice and the global `cordee/config.yml` settings (`batch-lines`, `risk`,
review waits), then points to `cordee/GETTING-STARTED.md` (daily developer cheat sheet) and `cordee/REFERENCE.md`
(complete human manual), both shipped in `template/cordee/`, replaced on upgrade, and left out of the markdown ratio.
_Rejected:_ a `--tokens` flag on `deploy` that omits the files (a second tree to test, and turning tokens on later
would need a new deploy instead of one line in `cordee/config.yml` and `install-hook`); keeping `tokens: true` as the
default (installs a `pre-push` network hook before the human has chosen it); pointing humans only to `WORKFLOW.md`
(written as terse operational instructions for agents, not as a progressive guide or full manual for humans).

## 80. CI checks the commit that removes the harness (2026-11-08)

`audit --range` skipped every commit without `cordee/bin/cordee`, there for the commits made before adoption. A push
that removes the harness in one commit and brings it back in the next, as a `deploy` gone wrong then put right does,
went through CI with that commit unchecked, and the hook, which passes in a repo without the harness, had not checked
it either. CI now skips a commit only when its parent lacks the harness too: the removal is judged like any batch,
which an agent's fails on its size, a human's only warns. A tip without the harness still fails CI, on the missing
script.
_Rejected:_ refusing any commit that removes `cordee/bin/` (removing the kit is a guided step, `guide/upgrade.md`); a
hook that fails when the script is missing (it runs in older branches and in other repos sharing the hook).

## 81. The ledger and the cockpit name the exact model (2026-11-08)

`usage` gave the ledger the model family, `opus` for `claude-opus-5-5`, and `report` showed the family too. An API of
environmental impact, or a price, needs the exact model: two versions of one family differ in both. `usage` and
`report` now name the model as the tool's log does, and `family()` goes. The notes already shared keep `opus`, and
`ledger report` shows them on lines of their own: a few weeks of history, which a reader sums by hand.
_Rejected:_ the family in the cockpit's local `report` only (a second name for one model, and the dev pays the
version, not the family); `v2` notes that `report` reads apart from `v1` (code to read old notes for a few weeks of
history); a call to an impact API (the data first, the tooling when someone needs it).

## 82. `deploy` refuses to run from a kit inside the repo (2026-11-08)

`deploy` ships in every repo's `cordee/bin/`. Run from there, `bash cordee/bin/cordee deploy`, it took the repo for the
kit: it deleted `cordee/bin/` and `cordee/guide/`, then stopped on a file copied onto itself, the harness gone and a
false tag in `cordee/README.md`. Run in the kit from `template/`, it overwrote the kit's launchers without a word. It
now stops first, when the template is the repo or a folder in it, and says to run it from a clone elsewhere.
_Rejected:_ dropping `deploy` from the copy (the upgrade runs the new kit's script, so the copy costs nothing and keeps
one tree); checking that the template holds `cordee/WORKFLOW.md` (every template does, the repo's copy too).

## 83. `Spec-Unchanged` names one module and gives a reason, or stops the commit (2026-11-08)

The check of the message split `Spec-Unchanged(a b): ...` into two modules and passed it, and passed
`Spec-Unchanged(a):` with nothing after the colon, while the rule that spares a module wants one name and a reason:
both ended in a DRIFT that told the author to add the very line they had written. The check now applies that rule and
stops the commit with an ERROR that names the fault: more than one name, no such module, or no reason.
_Rejected:_ sparing every module of a list (two ways to write one thing, and the workflow, the reference and the CI
already show one per line); a note that lets the commit go on (the module is still unspared, so the DRIFT follows).
