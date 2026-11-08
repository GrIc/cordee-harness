"""The mechanical part of a deploy, run from the kit's clone in the repo that gets it. The agent merges the rest."""
import os
import re
import shutil
import sys

from harness import hooks
from harness.git import git, try_git

CI = {"github": ".github/workflows/cordee.yml", "gitlab": ".gitlab-ci.yml"}


def deploy(source, tag, forge=None):
    template = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.chdir(git("rev-parse", "--show-toplevel"))
    forge = forge or forge_of(try_git("remote", "get-url", "origin") or "")
    if forge not in CI:
        sys.exit("Cannot tell the forge from origin: ask the human whether it is GitHub or GitLab, then run deploy again"
                 " with --forge github or --forge gitlab.")
    copied, present = [], []
    for folder, _, names in os.walk(template):
        for name in names:
            path = os.path.relpath(os.path.join(folder, name), template).replace(os.sep, "/")
            if path in CI.values() and path != CI[forge]:
                continue
            if os.path.lexists(path):
                present.append(path)
                continue
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            shutil.copy2(os.path.join(folder, name), path)
            copied.append(path)
    if "cordee/README.md" in copied:
        with open("cordee/README.md", encoding="utf-8", newline="") as file:
            text = file.read()
        with open("cordee/README.md", "w", encoding="utf-8", newline="") as file:
            file.write(text.replace("<source> <tag>", f"{source} {tag}", 1))
    print(f"Copied {len(copied)} files of Cordee {tag}, with the CI file for {forge}.")
    if present:
        print("Already in the repo, to merge as the deploy says:")
        for path in sorted(present):
            print(f"  {path}")
    return hooks.install()


def forge_of(url):
    """github or gitlab when the host of the URL names it, as https://host/..., ssh://user@host/... or user@host:..."""
    host = re.sub(r"^[a-z+]+://", "", url).split("/")[0].split("@")[-1].split(":")[0].lower()
    return next((forge for forge in CI if forge in host), None)
