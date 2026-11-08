"""What a dev pastes in a bug report: the kit, the platform, the hooks, the ledger, the logs read and an audit's time.
A line starting with NOTE says what to fix."""
import os
import platform
import re
import subprocess
import time

from fabrik import VERSION
from fabrik.git import git, try_git
from fabrik.hooks import HOOKS
from fabrik.logs import READERS

DAYS = 30


def doctor():
    print(f"sdd-fabrik {VERSION}, Python {platform.python_version()}, {git('--version')}, "
          f"{platform.system()} {platform.release()}")
    deployed = deployed_tag()
    if deployed and deployed.lstrip("v") != VERSION:
        print(f"NOTE sdd/README.md says it was deployed from {deployed}, the kit's files are {VERSION}: finish the "
              "upgrade (sdd/guide/upgrade.md), or fix its first line.")
    folder = git("rev-parse", "--git-path", "hooks")
    print(f"hooks: {folder}" + (" (core.hooksPath)" if try_git("config", "core.hooksPath") else ""))
    for name, command in missing(folder):
        print(f"NOTE the {name} hook does not run {command}: run bash sdd/bin/sdd install-hook, and add "
              "the line it prints if it does not write the hook itself.")
    if try_git("check-ignore", "-q", "QUIZ.md") is None:
        print("NOTE QUIZ.md is not kept out of git: run bash sdd/bin/sdd install-hook.")
    print("ledger: " + ("off (git config sdd.ledger false)" if try_git("config", "--bool", "sdd.ledger") == "false"
                        else "on"))
    repo, end = git("rev-parse", "--show-toplevel"), int(time.time())
    replies = {reader.__name__.rsplit(".", 1)[-1]: sum(1 for _ in reader.usage(repo, end - DAYS * 86400, end))
               for reader in READERS}
    print(f"replies read in {DAYS} days: " + ", ".join(f"{name} {count}" for name, count in replies.items()))
    start = time.monotonic()
    subprocess.run(["sh", "sdd/bin/sdd", "audit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"audit: {time.monotonic() - start:.1f} s")


def missing(folder):
    """Each command of the kit's hooks that the hook of that name in folder does not run, as (hook, command)."""
    return [(name, command) for name, _, commands in HOOKS for command in commands
            if command not in read(os.path.join(folder, name))]


def deployed_tag():
    """The tag the first line of sdd/README.md names, None in a repo without one, such as the kit's own."""
    found = re.match(r"Deployed from \S+ (\S+?)\.?$", read("sdd/README.md").split("\n", 1)[0])
    return found and found.group(1)


def read(path):
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as file:
        return file.read()
