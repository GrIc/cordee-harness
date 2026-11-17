"""Learning a module the dev did not write: a quiz on its code at a commit, graded without a commit
(cordee/guide/learn.md). It lives apart from a batch's quiz, so that one can wait beside it."""
import os
import sys

from harness import contracts, hooks, journal, quiz
from harness.git import git

LEARN = "LEARN.md"


def start(module):
    """Before the quiz: the line that starts its key, and the two paths to write."""
    contract = f"cordee/modules/{module}.md"
    if not os.path.isfile(contract):
        sys.exit(f"No {contract}: write the module's contract first (cordee/guide/learn.md).")
    hooks.exclude(f"/{LEARN}")
    os.makedirs(os.path.dirname(key_path()), exist_ok=True)
    print(f"fingerprint: learn {module} {git('rev-parse', 'HEAD')}")
    print(f"quiz: {LEARN}")
    print(f"key: {key_path()}")


def audit():
    """The reviewer's part, so that a malformed quiz never reaches the dev."""
    module, found = form()
    ranks = "".join(question.right for question in found)
    if len(ranks) > 1 and ranks == ranks[0] * len(ranks):
        print(f"NOTE {LEARN}: the right answer is box {ranks[0]} every time, vary it.", file=sys.stderr)
    print(f"OK: {LEARN} and its key fit {module}.")


def grade():
    """The dev's part: the boxes ticked against the key. Once all are right, the questions the dev flagged go to the
    quiz journal, on the module learned, and the quiz goes."""
    module, found = form()
    quiz.answers(found, LEARN, key_path(), "run bash cordee/bin/cordee learn --grade again")
    journal.write(module, LEARN)
    os.remove(LEARN)
    os.remove(key_path())
    print(f"{len(found)}/{len(found)}: {module} learned.")


def form():
    """The module the key is for and the questions of LEARN.md, each citing places in the files the module governs or
    the tests its contract links, at the commit the quiz was written on. A module's contract is read from the disk:
    the dev may learn it before committing it."""
    key = key_path()
    if not (os.path.isfile(LEARN) and os.path.isfile(key)):
        sys.exit(f"No quiz to learn a module: run bash cordee/bin/cordee learn <module>, then the reviewer writes"
                 f" {LEARN} and its key (cordee/guide/learn.md).")
    first = quiz.read_lines(key)[:1]
    if not first or not first[0].startswith("learn ") or first[0].count(" ") != 2:
        sys.exit(f"{key} starts with the fingerprint line bash cordee/bin/cordee learn <module> prints.")
    _, module, commit = first[0].split(" ")
    if commit != git("rev-parse", "HEAD"):
        print(f"NOTE HEAD moved since {LEARN} was written: its See lines point at the code as it was then.",
              file=sys.stderr)
    contract = f"cordee/modules/{module}.md"
    if not os.path.isfile(contract):
        sys.exit(f"No {contract}: go back to a branch that has it, or run bash cordee/bin/cordee learn <module> again.")
    contracts.from_disk(commit, contract)
    governed = [path.rstrip("/") for path in contracts.governs(f"{commit}:{contract}")]
    tests = {path for _, _, path in contracts.contract_links(commit, contract)}

    def fits(file, first, last):
        text = contracts.show(f"{commit}:{file}")
        mine = file in tests or any(file == path or file.startswith(path + "/") for path in governed)
        return mine and text is not None and 0 < first and last <= text.count("\n") + 1

    found = quiz.questions(LEARN, key)
    if not 1 <= len(found) <= 3:
        sys.exit(f'{LEARN} needs 1 to 3 questions, each under a "## " heading.')
    quiz.shape(found, fits, f"in the files {module} governs or the tests its contract links")
    return contracts.module(contract), found


def key_path():
    return git("rev-parse", "--git-path", "cordee/learn-key")
