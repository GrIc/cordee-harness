"""What a contract says: the paths it governs, its risk, its links to tests."""
import posixpath
import re

from fabrik.git import git, lines, try_git


def governs(revision):
    """The paths a contract governs, at a revision path such as HEAD:sdd/modules/search.md."""
    paths, inside = [], False
    for line in front_matter(re.sub("[\"']", "", git("show", revision))):
        inside = inside or line.startswith("governs:")
        if inside:
            paths += re.sub(r"[][,]", " ", re.sub(r"^governs:\s*", "", line)).split()
            inside = "]" not in line
    return paths


def front_matter(text):
    """The lines between the first two --- lines."""
    found, fence = [], 0
    for line in text.replace("\r", "").split("\n"):
        if re.match(r"---\s*$", line):
            fence += 1
        elif fence == 1:
            found.append(line)
    return found


def risky(revision):
    """Whether the contract at a revision path declares risk: high."""
    text = try_git("show", revision)
    return text is not None and any(re.match(r"risk:\s*high\s*$", line) for line in front_matter(text))


def contracts(tree):
    return [path for path in lines(git("ls-tree", "-r", "--name-only", tree, "sdd/modules/")) if path.endswith(".md")]


def module(contract):
    return posixpath.basename(contract)[: -len(".md")]


def modules(tree):
    """The modules of a tree, for a message."""
    names = lines(git("ls-tree", "--name-only", tree, "sdd/modules/"))
    return ", ".join(module(name) for name in names if name.endswith(".md"))


def links(tree, contract):
    """Drift between a contract and the tests it links: a linked file the tree lacks, or a name the file lacks."""
    found = []
    text = re.sub(" +", " ", re.sub("[\r\n]", " ", git("show", f"{tree}:{contract}")))
    for link in re.findall(r"\[[^]]*\]\([^)]*\)", text):
        name, target = link[1:].split("](", 1)
        target = target[:-1].split("#")[0]
        if not target or ":" in target or target.endswith((".md", "/")):
            continue
        # A target starts at the repo root or is relative to the contract. Resolved here, not by git -C: in a
        # worktree's hook, git -C takes the contract's folder for the work tree.
        path = target[1:] if target.startswith("/") else resolve(posixpath.dirname(contract), target)
        file = path and try_git("ls-tree", "--name-only", tree, "--", path)
        if not file:
            found.append(f'DRIFT {contract}: links "{name}" to {target}, a file the commit does not have.')
        # The name as whole words, as grep -w finds it.
        elif (git("cat-file", "-t", f"{tree}:{file}") == "blob" and name not in (posixpath.basename(file), file)
              and not re.search(rf"(?<!\w){re.escape(name)}(?!\w)", git("show", f"{tree}:{file}"))):
            found.append(f'DRIFT {contract}: links "{name}", not found in {file}.')
    return found


def resolve(folder, target):
    """The path of target from folder, or "" when it climbs out of the repo."""
    kept = []
    for part in f"{folder}/{target}".split("/"):
        if part == "..":
            if not kept:
                return ""
            kept.pop()
        elif part not in (".", ""):
            kept.append(part)
    return "/".join(kept)
