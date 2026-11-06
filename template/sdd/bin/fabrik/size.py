"""The size of a batch: its lines of code and tests, and its modules."""
import re
import sys

from fabrik.contracts import config
from fabrik.git import git, lines

# The lines of code and tests an agent batch may change when sdd/config.yml sets no batch-lines. Up to 5% over only
# gets a note.
MAX_LINES = 200

# Files that ask no quiz when a batch changes only them, outside every module: prose and the files git itself reads.
PROSE_OR_GIT = re.compile(r"\.md$|(^|/)\.git(ignore|attributes|keep)$")

# Files that count neither in the size nor in what the quiz covers: those, and lock files.
NOT_CODE = re.compile(PROSE_OR_GIT.pattern + r"|\.lock$|lock\.json$|lock\.yaml$")


def size(batch, base, tree, message):
    """Notes in batch what is over the limits from base to tree, counting the modules drift found touched."""
    count = 0
    for line in lines(git("diff", "--numstat", "--no-renames", base, tree)):
        added, deleted, path = line.split("\t", 2)
        if added != "-" and not NOT_CODE.search(path):
            count += int(added) + int(deleted)
    limit = batch_lines(base, tree)
    if re.search(r"^Large-Batch:[^\S\n]*\S", message, re.M):
        if count > limit:
            batch.notes += f"NOTE {count} changed lines of code and tests, over {limit}: Large-Batch lifts it.\n"
        if batch.touched > 1:
            batch.notes += f"NOTE the batch changes code of {batch.touched} modules: Large-Batch lifts it.\n"
        return
    if count > limit * 105 // 100:
        batch.findings += (f"SIZE {count} changed lines of code and tests, over {limit} by more than 5%.\n"
                           "      Split the batch, or the human adds 'Large-Batch: <reason>' to the message.\n")
    elif count > limit:
        batch.notes += f"NOTE {count} changed lines of code and tests, over {limit} but within 5%.\n"
    if batch.touched > 1:
        batch.findings += (f"SIZE the batch changes code of {batch.touched} modules.\n"
                           "      Split it by module, or the human adds 'Large-Batch: <reason>' to the message.\n")


def batch_lines(base, tree):
    """The repo's limit, the smaller of the parent's and the batch's own: a batch cannot raise the limit it is judged
    on."""
    own = config(tree, "batch-lines") or str(MAX_LINES)
    if not re.fullmatch(r"[0-9]+", own):
        sys.exit(f"ERROR sdd/config.yml: batch-lines is {own}. Write a number of lines, such as 200.")
    # A parent committed past the hook with a wrong value counts as the default, so that the batch fixing it passes.
    parent = config(base, "batch-lines") or ""
    return min(int(own), int(parent) if re.fullmatch(r"[0-9]+", parent) else MAX_LINES)
