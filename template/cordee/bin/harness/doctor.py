"""What a dev pastes in a bug report: the kit, the platform, the hooks, the ledger, the logs read and an audit's time.
A line starting with NOTE says what to fix."""
import os
import platform
import re
import subprocess
import time

from harness import VERSION
from harness.git import git, try_git
from harness.hooks import HOOKS
from harness.logs import READERS

DAYS = 30


def doctor():
    print(f"cordee {VERSION}, Python {platform.python_version()}, {git('--version')}, "
          f"{platform.system()} {platform.release()}")
    deployed = deployed_tag()
    if deployed and deployed.lstrip("v") != VERSION:
        print(f"NOTE cordee/README.md says it was deployed from {deployed}, the kit's files are {VERSION}: finish the "
              "upgrade (cordee/guide/upgrade.md), or fix its first line.")
    folder = git("rev-parse", "--git-path", "hooks")
    print(f"hooks: {folder}" + (" (core.hooksPath)" if try_git("config", "core.hooksPath") else ""))
    for name, command in missing(folder):
        print(f"NOTE the {name} hook does not run {command}: run bash cordee/bin/cordee install-hook, and add "
              "the line it prints if it does not write the hook itself.")
    if try_git("check-ignore", "-q", "QUIZ.md") is None:
        print("NOTE QUIZ.md is not kept out of git: run bash cordee/bin/cordee install-hook.")
    off = try_git("config", "--bool", "cordee.ledger") == "false"
    print("ledger: " + ("off (git config cordee.ledger false)" if off else "on"))
    repo, end = git("rev-parse", "--show-toplevel"), int(time.time())
    replies = {reader.__name__.rsplit(".", 1)[-1]: sum(1 for _ in reader.usage(repo, end - DAYS * 86400, end))
               for reader in READERS}
    print(f"replies read in {DAYS} days: " + ", ".join(f"{name} {count}" for name, count in replies.items()))
    start = time.monotonic()
    subprocess.run(["sh", "cordee/bin/cordee", "audit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"audit: {time.monotonic() - start:.1f} s")


def missing(folder):
    """Each command of the kit's hooks that the hook of that name in folder does not run, as (hook, command)."""
    return [(name, command) for name, _, commands in HOOKS for command in commands
            if command not in read(os.path.join(folder, name))]


def deployed_tag():
    """The tag the first line of cordee/README.md names, None in a repo without one, such as the kit's own."""
    found = re.match(r"Deployed from \S+ (\S+?)\.?$", read("cordee/README.md").split("\n", 1)[0])
    return found and found.group(1)


def read(path):
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as file:
        return file.read()
