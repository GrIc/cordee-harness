"""A repo's code by folder, and how much of it a contract governs: where to read first in code that lived before the
harness, and which contracts are still to write (cordee/guide/discover.md)."""
import posixpath
from collections import Counter, defaultdict

from harness.contracts import contracts, governs, module
from harness.git import git, lines, try_git
from harness.size import PROSE_OR_GIT

# The folders shown, largest first: past them, a line counts the rest.
ROWS = 15


def discover(folder):
    """The tracked files below a folder of the repo, the whole repo without one, summed by the folders it holds."""
    top = git("rev-parse", "--show-toplevel")
    prefix = folder.strip("/") + "/" if folder.strip("/") else ""
    files = lines(git("ls-files", "--", prefix or ".", cwd=top))
    owner = {}
    if try_git("rev-parse", "-q", "--verify", "HEAD") is not None:
        for contract in contracts("HEAD"):
            for path in lines(git("ls-files", "--", *governs(f"HEAD:{contract}"), cwd=top)):
                owner[path] = module(contract)
    rows, here = defaultdict(lambda: [0, 0, 0, Counter(), {}]), []
    for path in files:
        name, _, rest = path[len(prefix):].partition("/")
        row = rows[name + "/" if rest else "(files here)"]
        if PROSE_OR_GIT.search(path):
            row[2] += 1
            if not rest and not name.startswith(".git"):
                here.append(name)
            continue
        row[0] += 1
        row[3][posixpath.splitext(path)[1].lstrip(".") or "-"] += 1
        if path in owner:
            row[1] += 1
            row[4][owner[path]] = None
    code, governed = (sum(row[i] for row in rows.values()) for i in (0, 1))
    print(f"{prefix or 'The repo'}: {code} files of code, {governed} in a module"
          + (f" ({governed * 100 // code}%)." if code else "."))
    print(f"{'folder':32}{'code':>7}{'module':>8}{'prose':>7}  kinds, modules")
    ranked = sorted(rows.items(), key=lambda item: (-item[1][0], item[0]))
    for name, (count, inside, prose, kinds, modules) in ranked[:ROWS]:
        told = ", ".join(f"{kind} {files}" for kind, files in kinds.most_common(3))
        print(f"{name[:31]:32}{count:>7}{inside:>8}{prose:>7}  " + "; ".join(filter(None, [told, ", ".join(modules)])))
    if len(ranked) > ROWS:
        print(f"and {len(ranked) - ROWS} smaller folders, {sum(row[0] for _, row in ranked[ROWS:])} files of code.")
    if here:
        print(f"Prose here: {', '.join(here[:12])}" + (f" and {len(here) - 12} more." if len(here) > 12 else "."))
