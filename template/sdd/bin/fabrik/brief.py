"""What waits for the dev before a batch. It names authors to coordinate, never to measure, and never fetches."""
import itertools
import os
import time
from collections import Counter

from fabrik.contracts import governs
from fabrik.git import exists, git, lines, me, try_git

# A pushed branch waits for a review once its last commit is this old.
REVIEW_WAIT_HOURS = 4


def brief(module):
    """Before a batch, in a module if given."""
    address = me(strict=True)
    for line in itertools.islice(waiting(address), 3):
        print(line)
    if module:
        for line in newcomer(address, module):
            print(line)


def waiting(address):
    """A quiz in another worktree of the clone, then the remote branches not merged by another dev, oldest first."""
    top = git("rev-parse", "--show-toplevel")
    for line in lines(git("worktree", "list", "--porcelain")):
        path = line[len("worktree "):]
        if line.startswith("worktree ") and os.path.isfile(f"{path}/QUIZ.md") and not os.path.samefile(path, top):
            yield f"A quiz waits for your answers in {path}."
    if try_git("rev-parse", "-q", "--verify", "refs/remotes/origin/HEAD") is None:
        return
    refs = git("for-each-ref", "--no-merged=origin/HEAD", "--sort=committerdate", "--format=%(refname)",
               "refs/remotes/origin")
    for ref in lines(refs):
        when, email, name = git("log", "-1", "--format=%ct%x09%aE%x09%aN", ref).split("\t", 2)
        hours = (int(time.time()) - int(when)) // 3600
        if hours >= REVIEW_WAIT_HOURS and email.lower() != address.lower():
            age = f"{hours} hours" if hours < 48 else f"{hours // 24} days"
            yield f"{ref[len('refs/remotes/'):]} waits for a review for {age}, see {name}."


def newcomer(address, module):
    """When it is the dev's first batch in a module, says so and who delivered there most, by name, to know whom to
    ask. Says nothing in a module the dev knows, or one not committed yet."""
    contract = f"sdd/modules/{module}.md"
    if not exists(f"HEAD:{contract}"):
        return []
    authors = Counter()
    log = git("log", "--no-merges", "--format=%aE%x09%aN", "--", contract, *governs(f"HEAD:{contract}"))
    for email, name in (line.split("\t") for line in lines(log)):
        if email.lower() == address.lower():
            return []
        authors[name] += 1
    if not authors:
        return []
    most = sorted(authors.items(), key=lambda author: (-author[1], author[0].casefold()))[:3]
    return [f"First batch of yours in {module}.", f"Who delivered there most: {', '.join(name for name, _ in most)}."]
