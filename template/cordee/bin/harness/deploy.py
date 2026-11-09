"""The mechanical part of a deploy or an upgrade, run from the kit's clone in the repo that gets it."""
import os
import re
import shutil
import sys

from harness import hooks
from harness.git import git, try_git

CI = {"github": ".github/workflows/cordee.yml", "gitlab": ".gitlab-ci.yml"}
KIT_DOCS = ("cordee/WORKFLOW.md", "cordee/GETTING-STARTED.md", "cordee/REFERENCE.md")
MARKER = r"<!-- (?:cordee|sdd-fabrik) -->.*?<!-- /(?:cordee|sdd-fabrik) -->"
STAMP = r"^Deployed from [^\n]*"


def deploy(source, tag, forge=None):
    template = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    top = os.path.realpath(git("rev-parse", "--show-toplevel"))
    # Run from the repo's own cordee/bin, or from the kit in the kit, it would delete the very files it copies. Not
    # commonpath: it fails on Windows when the kit's clone is on another drive.
    if os.path.normcase(os.path.join(template, "")).startswith(os.path.normcase(os.path.join(top, ""))):
        sys.exit("deploy copies the kit into this repo, so it runs from the kit's own clone, outside it: clone the kit"
                 " elsewhere, then run bash <clone>/template/cordee/bin/cordee deploy <source> <tag> here.")
    os.chdir(top)
    forge = forge or forge_of(try_git("remote", "get-url", "origin") or "")
    if forge not in CI:
        sys.exit("Cannot tell the forge from origin: ask the human whether it is GitHub or GitLab, then run deploy again"
                 " with --forge github or --forge gitlab.")
    with open(os.path.join(template, "AGENTS.md"), encoding="utf-8", newline="") as file:
        block = re.search(MARKER, file.read(), re.DOTALL).group(0)
    stamp = f"Deployed from {source} {tag}."
    for folder in ("cordee/bin", "cordee/guide"):
        shutil.rmtree(folder, ignore_errors=True)
    copied, present = [], []
    for folder, folders, names in os.walk(template):
        # A Python run without -B leaves its bytecode in the kit's clone, with the clone's path on that machine.
        folders[:] = [name for name in folders if name != "__pycache__"]
        for name in names:
            path = os.path.relpath(os.path.join(folder, name), template).replace(os.sep, "/")
            if path in CI.values() and path != CI[forge]:
                continue
            if name == ".gitkeep" and os.path.lexists(os.path.dirname(path)):
                continue
            if os.path.lexists(path) and path not in KIT_DOCS:
                if (path == "AGENTS.md" and replace_mark(path, MARKER, block)
                        or path == "cordee/README.md" and replace_mark(path, STAMP, stamp)):
                    copied.append(path)
                else:
                    present.append(path)
                continue
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            shutil.copy2(os.path.join(folder, name), path)
            if path == "cordee/README.md":
                replace_mark(path, STAMP, stamp)
            copied.append(path)
    print(f"Copied {len(copied)} files of Cordee {tag}, with the CI file for {forge}.")
    if present:
        print("Already in the repo, left as they are:")
        for path in sorted(present):
            print(f"  {path}")
    return hooks.install()


def forge_of(url):
    """github or gitlab when the host of the URL names it, as https://host/..., ssh://user@host/... or user@host:..."""
    host = re.sub(r"^[a-z+]+://", "", url).split("/")[0].split("@")[-1].split(":")[0].lower()
    return next((forge for forge in CI if forge in host), None)


def replace_mark(path, pattern, replacement):
    """Replaces the first match of pattern in path with replacement, and tells whether it found one."""
    if not os.path.isfile(path):
        return False
    with open(path, encoding="utf-8", newline="") as file:
        text = file.read()
    updated, count = re.subn(pattern, lambda _: replacement, text, count=1, flags=re.DOTALL)
    if not count:
        return False
    with open(path, "w", encoding="utf-8", newline="") as file:
        file.write(updated)
    return True
