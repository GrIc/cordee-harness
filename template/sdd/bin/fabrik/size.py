"""The size of a batch: its lines of code and tests, and its modules."""
import re
import sys

from fabrik.contracts import config, listed, matches, own_setting
from fabrik.git import git, lines

# The lines of code and tests an agent batch may change when sdd/config.yml sets no batch-lines. Up to 5% over only
# gets a note.
MAX_LINES = 200

# Files that ask no quiz when a batch changes only them, outside every module: prose and the files git itself reads.
PROSE_OR_GIT = re.compile(r"\.md$|(^|/)\.git(ignore|attributes|keep)$")

# Files that count neither in the size nor in what the quiz covers, besides those, when sdd/config.yml lists none
# under not-code: lock files.
NOT_CODE = ["/\\.lock$/", "/lock\\.json$/", "/lock\\.yaml$/"]


def not_code(base, tree):
    """Whether a path counts neither in the size nor in what the quiz covers: prose, git's own files, and the files
    not-code lists in both trees, so that a batch widening the list is judged by the old one."""
    found = [listed(tree, "not-code", NOT_CODE, True), listed(base, "not-code", NOT_CODE, False)]
    return lambda path: bool(PROSE_OR_GIT.search(path)) or all(
        any(matches(entry, path) for entry in entries) for entries in found)


def size(batch, base, tree, message):
    """Notes in batch what is over the limits from base to tree, counting the modules drift found touched."""
    count = 0
    for line in lines(git("diff", "--numstat", "--no-renames", base, tree)):
        added, deleted, path = line.split("\t", 2)
        if added != "-" and not batch.not_code(path):
            count += int(added) + int(deleted)
    limit, where = batch_lines(batch, base, tree)
    if re.search(r"^Large-Batch:[^\S\n]*\S", message, re.M):
        if count > limit:
            batch.notes += (f"NOTE {count} changed lines of code and tests, over {limit} ({where}): Large-Batch lifts"
                            " it.\n")
        if batch.touched > 1:
            batch.notes += f"NOTE the batch changes code of {batch.touched} modules: Large-Batch lifts it.\n"
        return
    if count > limit * 105 // 100:
        batch.findings += (f"SIZE {count} changed lines of code and tests, over {limit} ({where}) by more than 5%.\n"
                           "      Split the batch, or the human adds 'Large-Batch: <reason>' to the message.\n")
    elif count > limit:
        batch.notes += f"NOTE {count} changed lines of code and tests, over {limit} ({where}) but within 5%.\n"
    if batch.touched > 1:
        batch.findings += (f"SIZE the batch changes code of {batch.touched} modules.\n"
                           "      Split it by module, or the human adds 'Large-Batch: <reason>' to the message.\n")


def batch_lines(batch, base, tree):
    """The limit of the batch and where it is set: the contract of a module whose code it changes, else
    sdd/config.yml, else the kit's default. Every contract of the batch is judged, for its note."""
    repo = judged(batch, "sdd/config.yml", config(tree, "batch-lines"), config(base, "batch-lines"),
                  (MAX_LINES, "the kit's default"))
    modules = {}
    for contract in (f"sdd/modules/{name}.md" for name in batch.hit):
        modules[contract] = judged(batch, contract, own_setting(f"{tree}:{contract}", "batch-lines"),
                                   own_setting(f"{base}:{contract}", "batch-lines"), repo)
    return min([modules[contract] for contract in batch.coded] or [repo])


def judged(batch, path, own, parent, default):
    """The limit a file sets, as (lines, where), the default when unset. A value the batch changes holds at once, and
    gets a note in batch, so that the human sees an agent giving itself more room."""
    if own and not re.fullmatch(r"[0-9]+", own):
        sys.exit(f"ERROR {path}: batch-lines is {own}. Write a number of lines, such as 200.")
    limit = (int(own), f"batch-lines in {path}") if own else default
    # A parent committed past the hook with a wrong value counts as the default.
    before = int(parent) if parent and re.fullmatch(r"[0-9]+", parent) else default[0]
    if before != limit[0]:
        batch.notes += f"NOTE {path}: batch-lines goes from {before} to {limit[0]} in this batch.\n"
    return limit
