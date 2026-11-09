"""What a contract says: the paths it governs, its settings, its links to tests."""
import functools
import posixpath
import re
import sys

from harness.git import git, lines, run, try_git


def governs(revision):
    """The paths a contract governs, at a revision path such as HEAD:cordee/modules/search.md. YAML writes them as a
    list in brackets that may wrap, as "- path" lines below the key, or as one path; the next key ends them, comments are
    no paths. An absolute path or one outside the repo stops the command, since git would refuse every diff."""
    value, inside = [], False
    for line in front_matter(re.sub("[\"']", "", show(revision) or "")):
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


RISKS = ("none", "normal", "high")


def risk(tree, contract, checked):
    """The risk of a contract in a tree: its own, else that of cordee/config.yml in the same tree, else normal; the
    repo's alone without a contract, None when the contract is not there. Another value stops the command when checked (the
    tree), and counts as normal otherwise (the base), so that the commit fixing it passes."""
    own = None
    if contract:
        text = show(f"{tree}:{contract}")
        if text is None:
            return None
        own = value(front_matter(text), "risk")
    found = own or config(tree, "risk") or "normal"
    if found in RISKS:
        return found
    if checked:
        sys.exit(f"ERROR {contract if own else 'cordee/config.yml'}: risk is {found}."
                 " Write none, normal or high.")
    return "normal"


def highest(risks):
    return max(risks, key=RISKS.index)


def own_setting(revision, key):
    """A setting the contract at a revision path states itself, None when it does not or is not there."""
    return value(front_matter(show(revision) or ""), key)


def config(tree, key):
    """A setting of the repo in cordee/config.yml of the tree, None without one."""
    return value(lines(show(f"{tree}:cordee/config.yml") or ""), key)


def value(text_lines, key):
    """The value of a flat key: value line, without its quotes or its comment."""
    for line in text_lines:
        found = re.match(rf"{re.escape(key)}:(.*)", re.sub(r"(^|\s)#.*", "", line))
        if found:
            return found.group(1).strip().strip("\"'")
    return None


# The files that steer the project or the harness, when cordee/config.yml lists none.
SENSITIVE = ["cordee/bin/", "cordee/WORKFLOW.md", "cordee/guide/", "cordee/config.yml",
             "/(?i)(^|/)(agents|claude)\\.md$/", "cordee/architecture.md", "cordee/coding-style.md", "cordee/product.md",
             "cordee/modules/", ".github/workflows/", ".gitlab-ci.yml", ".claude/", "opencode.json", "kilo.jsonc", ".vscode/settings.json"]


def sensitive(tree, checked):
    """The sensitive entries of a tree: those of cordee/config.yml, else the kit's, and those of every contract. A wrong
    entry stops the command when checked (the tree), and is left out otherwise (the base), so that the commit fixing it
    passes."""
    found = listed(tree, "sensitive", SENSITIVE, checked)
    for contract in contracts(tree):
        found += entries(front_matter(show(f"{tree}:{contract}") or ""), contract, checked) or []
    return found


def listed(tree, key, default, checked):
    """The entries cordee/config.yml of a tree lists under a key, else the kit's default list."""
    found = entries(lines(show(f"{tree}:cordee/config.yml") or ""), "cordee/config.yml", checked, key)
    return list(default) if found is None else found


def entries(text_lines, where, checked, key="sensitive"):
    """The entries a file lists under a key, one on the key's line or one per "- " line below it, never split; None
    when the key is not there."""
    found, inside = None, False
    for line in text_lines:
        line = re.sub(r"(^|\s)#.*", "", line)
        if re.match(r"[^\s-]", line):
            inside = line.startswith(f"{key}:")
            entry = line[len(key) + 1:] if inside else ""
            found = [] if inside else found
        else:
            item = re.match(r"\s*-\s(.*)", line)
            entry = item.group(1) if inside and item else ""
        entry = entry.strip().strip("\"'")
        if entry in ("", "[]"):
            continue
        if entry.startswith("["):
            if checked:
                example = entry[1:].split(",")[0].strip(" ]") or "cordee/architecture.md"
                sys.exit(f'ERROR {where}: {key} is {entry}. Write one entry per line below the key, as'
                         f' "  - {example}".')
            continue
        if re.fullmatch("/.+/", entry):
            try:
                re.compile(entry[1:-1])
            except re.error as error:
                if checked:
                    sys.exit(f"ERROR {where}: {key} lists {entry}, a regular expression that does not compile"
                             f" ({error}). Fix it, or write a path.")
                continue
        found.append(entry)
    return found


def matches(entry, path):
    """Whether an entry of a list such as sensitive matches a path: a regular expression between slashes where it is
    found, a folder every path under it, else the path itself."""
    if re.fullmatch("/.+/", entry):
        return re.search(entry[1:-1], path) is not None
    if entry.endswith("/") and not entry.startswith("/"):
        return path.startswith(entry)
    return path == entry


def contracts(tree):
    return [path for path, (kind, _) in tree_objects(tree).items()
            if kind == "blob" and path.startswith("cordee/modules/") and path.endswith(".md")]


def in_tree(tree, path):
    """Whether path (a file or a folder) is in tree."""
    return path.rstrip("/") in tree_objects(tree)


def module(contract):
    return posixpath.basename(contract)[: -len(".md")]


def modules(tree):
    """The modules of a tree, for a message."""
    return ", ".join(module(path) for path in contracts(tree) if "/" not in path[len("cordee/modules/"):])


def links(tree, contract):
    """The drift between a contract and the files it links to in a tree, other than Markdown and folders: a linked file
    the tree lacks, or a name the file lacks."""
    objects, found = tree_objects(tree), []
    for name, target, path in contract_links(tree, contract):
        kind, sha = objects.get(path, (None, None))
        if not kind:
            found.append(f'DRIFT {contract}: links "{name}" to {target}, a file the commit does not have.')
        elif kind == "blob":
            if sha not in BLOBS:
                # Files only: a submodule's commit is not in this repo, git cat-file --batch says it is missing.
                load_blobs(objects[p][1] for other in contracts(tree) for _, _, p in contract_links(tree, other)
                           if objects.get(p, (None,))[0] == "blob")
            # The name as whole words, as grep -w finds it.
            if name not in (posixpath.basename(path), path) and not re.search(rf"(?<!\w){re.escape(name)}(?!\w)",
                                                                              BLOBS[sha]):
                found.append(f'DRIFT {contract}: links "{name}", not found in {path}.')
    return found


def contract_links(tree, contract):
    text = re.sub(" +", " ", re.sub("[\r\n]", " ", show(f"{tree}:{contract}") or ""))
    for link in re.findall(r"\[[^]]*\]\([^)]*\)", text):
        name, target = link[1:].split("](", 1)
        target = target[:-1].split("#")[0]
        if target and ":" not in target and not target.endswith((".md", "/")):
            # A target starts at the repo root or is relative to the contract. Resolved here, not by git -C: in a
            # worktree's hook, git -C takes the contract's folder for the work tree.
            path = target[1:] if target.startswith("/") else resolve(posixpath.dirname(contract), target)
            yield name, target, path


BLOBS = {}


def show(revision):
    """The text of a blob at a revision path such as HEAD:cordee/config.yml, or None when it is not there."""
    tree, path = revision.split(":", 1)
    if not tree:
        return try_git("show", revision)
    kind, sha = tree_objects(tree).get(path, (None, None))
    if kind != "blob":
        return None
    load_blobs([sha])
    return BLOBS[sha]


@functools.cache
def tree_objects(tree):
    """The entries of a tree, as {path: (kind, sha)}, loading its config and contracts into BLOBS."""
    found = {}
    for line in lines(git("ls-tree", "--full-tree", "-r", "-t", tree)):
        meta, path = line.split("\t", 1)
        _, kind, sha = meta.split()
        found[path] = (kind, sha)
    load_blobs(sha for path, (kind, sha) in found.items()
               if kind == "blob" and (path == "cordee/config.yml" or path.startswith("cordee/modules/")))
    return found


def load_blobs(shas):
    missing = [sha for sha in dict.fromkeys(shas) if sha and sha not in BLOBS]
    if not missing:
        return
    out = run(["cat-file", "--batch"], input="\n".join(missing) + "\n").stdout
    pos = 0
    for sha in missing:
        end = out.index(b"\n", pos)
        size = int(out[pos:end].split()[2])
        BLOBS[sha] = out[end + 1:end + 1 + size].decode(errors="replace").rstrip("\n")
        pos = end + 1 + size + 1


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
