"""The quiz journal: the questions a dev flagged or commented, kept on this machine and shared by the clone's
worktrees. A line is v2, the time, the batch's modules, the causes, the title and the words, tab-separated; the
cockpit reads it."""
import hashlib
import os
import re
import time
from collections import Counter

from harness.drift import changes, touched
from harness.git import commit_or, empty_tree, git, lines, shared_path
from harness.quiz import QUIZ, fingerprint, key_path, read_lines, staged

CAUSES = ["not-understood", "unclear", "not-wanted"]


def committed():
    """After a commit: its quiz, once the commit exists, goes to the journal if it passed, then away. A later
    commit-msg hook that fails keeps the quiz, and a commit made with --no-verify leaves none behind for the next batch.
    The post-commit hook runs it; the next commit, audit and fingerprint do too, for a clone whose hooks predate it."""
    key = key_path()
    if not (os.path.isfile(QUIZ) and os.path.isfile(key) and commit_or("HEAD", None)):
        return
    commit = quizzed(read_lines(key)[:1], int(os.path.getmtime(key)))
    if commit is None:
        return
    if any(line.startswith("Quiz:") for line in git("log", "-1", "--format=%B", commit).split("\n")):
        write(",".join(module for module, _ in touched(commit)))
    os.remove(QUIZ)
    os.remove(key)


def quizzed(key, written):
    """The commit of the batch the key is for, made since the key was written: HEAD, or below a merge or a pull that
    came on top without the post-commit hook. None for a batch not committed yet."""
    # An amend builds on what HEAD was before it, not on HEAD^.
    if key == [fingerprint(git("rev-parse", "HEAD^{tree}"), commit_or("HEAD@{1}", "none"))]:
        return "HEAD"
    for line in lines(git("log", f"--since=@{written}", "--format=%H %T %P")):
        commit, tree, *parents = line.split(" ")
        if key == [fingerprint(tree, parents[0] if parents else "none")]:
            return commit
    return None


def reworked():
    """Before a new quiz: the questions flagged in a quiz left for a batch that changed since and was never committed
    go to the journal, on the modules staged now. A flag that got the batch redone would be lost with that quiz. Once
    per state of QUIZ.md: the reviewer may ask again for the same batch."""
    key = key_path()
    if not (os.path.isfile(QUIZ) and os.path.isfile(key)) or read_lines(key)[:1] in ([], [staged()]):
        return
    with open(QUIZ, "rb") as file:
        state = hashlib.sha1(file.read()).hexdigest()
    done = git("rev-parse", "--git-path", "cordee/quiz-journaled")
    if os.path.isfile(done) and read_lines(done) == [state]:
        return
    write(",".join(module for module, _ in changes(commit_or("HEAD", empty_tree()), git("write-tree"))))
    with open(done, "w", encoding="utf-8") as file:
        file.write(state + "\n")


def write(modules):
    """Appends a line per question of QUIZ.md the dev flagged or commented. It runs once the commit of a passed quiz
    exists, or before a new quiz replaces this one, when the boxes are the dev's last word. The block's boxes are read
    by their place, so in any language."""
    rows, title, causes, words, box = [], "", [], "", 0

    def close():
        if causes or words:
            fields = ["v2", str(int(time.time())), modules or "-", ",".join(causes) or "-", title, words or "-"]
            rows.append("\t".join(field.replace("\t", " ") for field in fields) + "\n")

    for line in read_lines(QUIZ):
        if line.startswith("## "):
            close()
            title, causes, words, box = re.sub(r"^## ([0-9]+\. )?", "", line), [], "", 0
        elif re.match(r"> - \[[ xX]\]", line):
            box += 1
            if re.match(r"> - \[[xX]\]", line) and box <= len(CAUSES):
                causes.append(CAUSES[box - 1])
        elif re.match(r"> - [^[]", line):
            # The words follow the label and its ":"; a label without one leaves no words.
            label = re.match(r"> - [^:]*:\s*", line)
            words = line[label.end():] if label else ""
    close()
    os.makedirs(os.path.dirname(path()), exist_ok=True)
    with open(path(), "a", encoding="utf-8", newline="") as file:
        file.writelines(rows)


def path():
    return shared_path("quiz-journal")


def flagged(start):
    """Per module, the quiz answers flagged unclear or not wanted since start, once per title and cause: a commit that
    fails after the quiz passed journals it again."""
    flags = set()
    if os.path.exists(path()):
        with open(path(), encoding="utf-8", errors="replace") as file:
            for line in file:
                fields = line.rstrip("\n").split("\t")
                if fields[0] == "v2" and int(fields[1]) > start:
                    flags.update((module, fields[4], cause) for module in fields[2].split(",") if module != "-"
                                 for cause in fields[3].split(",") if cause in ("unclear", "not-wanted"))
    return Counter(module for module, _, _ in flags)
