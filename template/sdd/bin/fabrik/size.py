"""The size of a batch: its lines of code and tests, and its modules."""
import re

from fabrik.git import git, lines

# An agent batch up to 5% over only gets a note.
MAX_LINES = 200

# Files that count neither in the size nor in what the quiz covers: prose and lock files.
NOT_CODE = re.compile(r"\.md$|\.lock$|lock\.json$|lock\.yaml$")


def size(batch, base, tree, message):
    """Notes in batch what is over the limits from base to tree, counting the modules drift found touched."""
    count = 0
    for line in lines(git("diff", "--numstat", "--no-renames", base, tree)):
        added, deleted, path = line.split("\t", 2)
        if added != "-" and not NOT_CODE.search(path):
            count += int(added) + int(deleted)
    if re.search(r"^Large-Batch:[^\S\n]*\S", message, re.M):
        if count > MAX_LINES:
            batch.notes += f"NOTE {count} changed lines of code and tests, over {MAX_LINES}: Large-Batch lifts it.\n"
        if batch.touched > 1:
            batch.notes += f"NOTE the batch changes code of {batch.touched} modules: Large-Batch lifts it.\n"
        return
    if count > MAX_LINES * 105 // 100:
        batch.findings += (f"SIZE {count} changed lines of code and tests, over {MAX_LINES} by more than 5%.\n"
                           "      Split the batch, or the human adds 'Large-Batch: <reason>' to the message.\n")
    elif count > MAX_LINES:
        batch.notes += f"NOTE {count} changed lines of code and tests, over {MAX_LINES} but within 5%.\n"
    if batch.touched > 1:
        batch.findings += (f"SIZE the batch changes code of {batch.touched} modules.\n"
                           "      Split it by module, or the human adds 'Large-Batch: <reason>' to the message.\n")
