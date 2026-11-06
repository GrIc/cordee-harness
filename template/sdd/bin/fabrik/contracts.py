"""What a contract says: the paths it governs, its settings, its links to tests."""
import posixpath
import re
import sys

from fabrik.git import git, lines, try_git


def governs(revision):
    """The paths a contract governs, at a revision path such as HEAD:sdd/modules/search.md. YAML writes them as a list
    in brackets that may wrap, as "- path" lines below the key, or as one path; the next key ends them, comments are
    no paths. An absolute path or one outside the repo stops the command, since git would refuse every diff."""
    value, inside = [], False
    for line in front_matter(re.sub("[\"']", "", git("show", revision))):
        # A YAML comment starts with a "#" at the start of the line or after a space.
        line = re.sub(r"(^|\s)#.*", "", line)
        if not line.strip():
            continue
        # A line flush with the keys, other than a "- path" one, starts the next key.
        if re.match(r"[^\s-]", line):
            inside = line.startswith("governs:")
        if inside:
            value.append(re.sub(r"^(governs:|\s*-\s)", " ", line))
    paths = re.sub(r"[][,]", " ", " ".join(value)).split()
    for path in paths:
        if path.startswith("/") or resolve("", path) is None:
            sys.exit(f"ERROR {revision.split(':', 1)[1]}: governs {path}, outside the repo. Write each path from the"
                     f" repo root.")
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
    """Whether the contract at a revision path is at high risk, by its own front matter or sdd/config.yml."""
    text = try_git("show", revision)
    return text is not None and setting(front_matter(text), revision.split(":", 1)[0], "risk") == "high"


def setting(contract_lines, tree, key):
    """A module's setting: its contract's front matter, else sdd/config.yml of the tree, else None. Both hold flat
    key: value lines."""
    return value(contract_lines, key) or value(lines(try_git("show", f"{tree}:sdd/config.yml") or ""), key)


def value(text_lines, key):
    """The value of a flat key: value line, without its quotes or its comment."""
    for line in text_lines:
        found = re.match(rf"{re.escape(key)}:(.*)", re.sub(r"(^|\s)#.*", "", line))
        if found:
            return found.group(1).strip().strip("\"'")
    return None


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
    """The path of target from folder, or None when it climbs out of the repo."""
    kept = []
    for part in f"{folder}/{target}".split("/"):
        if part == "..":
            if not kept:
                return None
            kept.pop()
        elif part not in (".", ""):
            kept.append(part)
    return "/".join(kept)
