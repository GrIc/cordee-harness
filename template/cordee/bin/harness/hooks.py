"""The commit-msg hook, and the install of the hooks."""
import os
import re
import sys

from harness import quiz
from harness.checks import check, report
from harness.contracts import value
from harness.git import commit_or, empty_tree, git, is_agent, lines, try_git
from harness.journal import committed


# Each hook's line, and the commands in it that a hook written by hand or by a hook manager must run too.
CORE_HOOKS = [("commit-msg", '[ ! -f cordee/bin/cordee ] || bash cordee/bin/cordee hook "$1" || exit 1',
               ["cordee/bin/cordee hook"]),
              ("post-commit", "[ ! -f cordee/bin/cordee ] || bash cordee/bin/cordee committed",
               ["cordee/bin/cordee committed"])]
TOKEN_HOOKS = [CORE_HOOKS[0],
               ("post-commit", f"{CORE_HOOKS[1][1]}; [ ! -f cordee/bin/ledger ] || bash cordee/bin/ledger record",
                ["cordee/bin/cordee committed", "cordee/bin/ledger record"]),
               ("pre-push", '[ ! -f cordee/bin/ledger ] || bash cordee/bin/ledger sync "$1"',
                ["cordee/bin/ledger sync"])]


def hook(message_file):
    # Finishing a merge or a cherry-pick: their commits were checked when first made.
    if any(os.path.isfile(git("rev-parse", "--git-path", head)) for head in ("MERGE_HEAD", "CHERRY_PICK_HEAD")):
        return
    committed()
    message = read_message(message_file)
    # An amend of a quizzed commit carries HEAD's Quiz trailer and no new QUIZ.md: judge the whole commit against HEAD^.
    quizzed = bool(re.search(r"^Quiz:[^\S\n]*[0-9]+/[0-9]+", message, re.M)) and not os.path.isfile(quiz.QUIZ)
    batch = check(commit_or("HEAD^" if quizzed else "HEAD", empty_tree()), git("write-tree"), message)
    # A quiz key written for this very batch says a reviewer quizzed it: an agent batch, whatever message the human
    # typed in their IDE. The trailer goes in, so that CI, the ledger and the history see it too.
    key = quiz.key_path()
    if not is_agent(message, batch.emails) and os.path.isfile(key) and quiz.read_lines(key)[:1] == [quiz.staged()]:
        git("interpret-trailers", "--in-place", "--trailer", "Agent-Assisted: yes", message_file)
        message = read_message(message_file)
        print("NOTE a quiz was written for this batch: Agent-Assisted: yes is added to the message.", file=sys.stderr)
    if not report(batch, message):
        sys.exit(1)
    # A reword, an amend of a quizzed commit, or an amend that changes no file leaves nothing to quiz on.
    asked = not quizzed and batch.changed and (batch.level != "none" or os.path.isfile(quiz.QUIZ))
    if not is_agent(message, batch.emails) or not asked:
        return
    if re.search(r"^Bypass-Quiz:[^\S\n]*\S", message, re.M):
        return
    if re.search(r"^Bypass-Quiz:[^\S\n]*$", message, re.M):
        print("Bypass-Quiz needs a reason after the colon: without one, the quiz is still asked.", file=sys.stderr)
    quiz.grade(batch)
    covered, total, _ = batch.coverage
    trailer = f"Quiz: {batch.count}/{batch.count}"
    if total:
        trailer += f", covers {covered}/{total}"
    git("interpret-trailers", "--in-place", "--if-exists", "replace", "--trailer", trailer, message_file)


def read_message(message_file):
    """The commit message, without git's comment lines."""
    with open(message_file, encoding="utf-8", errors="replace", newline="") as file:
        return "".join(line for line in file if not line.startswith("#"))


def install():
    """The quiz checks each commit; when tokens are on in cordee/config.yml, the token ledger notes each commit and is
    shared at each push."""
    exclude = git("rev-parse", "--git-path", "info/exclude")
    os.makedirs(os.path.dirname(exclude), exist_ok=True)
    os.makedirs(git("rev-parse", "--git-path", "cordee"), exist_ok=True)
    if not os.path.isfile(exclude) or "/QUIZ.md" not in quiz.read_lines(exclude):
        with open(exclude, "a+b") as file:
            file.seek(0)
            # A last line without its newline would end in /QUIZ.md.
            file.write(b"\n/QUIZ.md\n" if file.read()[-1:] not in (b"", b"\n") else b"/QUIZ.md\n")
    done = [install_one(name, line) for name, line, _ in active_hooks()]
    if tokens_on():
        print("The token ledger notes what agents spend on each module, never who:"
              " git config cordee.ledger false stops it.")
    else:
        pre_push = git("rev-parse", "--git-path", "hooks") + "/pre-push"
        if try_git("config", "core.hooksPath") is None and os.path.isfile(pre_push) and ours(pre_push):
            os.remove(pre_push)
    return 0 if all(done) else 1


def active_hooks():
    return TOKEN_HOOKS if tokens_on() else CORE_HOOKS


def tokens_on():
    """Whether cordee/config.yml turns the cockpit and the token ledger on."""
    path = os.path.join(git("rev-parse", "--show-toplevel"), "cordee/config.yml")
    text = quiz.read_lines(path) if os.path.isfile(path) else lines(try_git("show", "HEAD:cordee/config.yml") or "")
    return value(text, "tokens") == "true"


def install_one(name, line):
    """Writes a hook with a line, or prints the line for a hook it did not write. The line passes in a repo without the
    harness, such as an older branch or another repo sharing the hook."""
    path = git("rev-parse", "--git-path", "hooks") + "/" + name
    if try_git("config", "core.hooksPath") is not None or (os.path.exists(path) and not ours(path)):
        print(f"Your {name} hook is {path}, or the file your hook manager builds it from. Add this line to it:",
              file=sys.stderr)
        print(line, file=sys.stderr)
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as file:
        file.write(f"#!/bin/sh\n# cordee\n{line}\n")
    os.chmod(path, os.stat(path).st_mode | 0o111)
    print(f"Installed {path}.")
    return True


def ours(path):
    with open(path, encoding="utf-8", errors="replace", newline="") as file:
        return "# cordee" in file.read().split("\n")
