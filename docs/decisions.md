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
