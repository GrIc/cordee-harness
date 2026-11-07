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

## 55. At intent risk, a quiz when a contract moves (2026-11-06)

A team or a module that wants no question on code gets the step `intent`, between `low` and `normal`: a batch asks a
quiz only when it adds, deletes or changes the contract of a module at `intent`, and a fix under `Spec-Unchanged` asks
none. The owner asked for it after the comparison with Scion (decision 46), whose review reads the intent of a change
rather than every line. Decision 47 also named `governs`, `depends`, `sdd/architecture.md` and a second module: the
first two are in the contract, a second module's code that no `Spec-Unchanged` spares is drift until its contract
changes too, and `sdd/architecture.md` goes to the sensitive files, which ask a quiz at any risk.
_Rejected:_ a setting of its own for the levels a quiz asks (code, architecture, functional, run): one more knob to
explain, which pays only for a team wanting run questions without architecture ones; `low` for such modules (no quiz
even when the intent moves); any contract that moves (a contract of a module at `low`, in the same batch, asks
nothing on its own).

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

## 57. A batch of tests alone asks one step less (2026-11-06)

Three questions on a batch that only adds tests cost the human what a change of behavior costs, while the tests leave
what the product does as it was and the human reads them in the diff. A batch whose changed files are files a contract
links to, with only Markdown and git's own files that no module governs and no `sensitive` list matches beside them,
is judged one step lower: `high` gives `normal`, `normal` gives `intent`, `intent` gives `low`. The links are the
contract's own word for which files prove it, read in the batch: a test deleted with its link, or one no contract
links to yet, is code like any other. A contract may move with its tests, since a new test needs its link: at
`intent` such a batch then asks nothing, unless the contracts are sensitive, as the kit's list has them. A sensitive
file keeps its quiz at any step (56).
_Rejected:_ test files found by name (`test_*`, `*_spec.*`, `tests/`: every language names them its own way, and a
fixture or a helper there changes what every test checks); no quiz at all for tests (a test that asserts the wrong thing
locks a bug in, and at `high` the human still reads one to three questions); the base's links too (a batch that drops
a test and its link weakens the proof, and should ask what it asked before).

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
