"""Drift between the contracts and their code, and the modules a commit touches."""
import re
import sys

from fabrik.contracts import contracts, governs, links, module, modules, risky
from fabrik.git import commit_or, empty_tree, exists, git, lines


def drift(batch, base, tree, message):
    """Notes in batch the modules whose code or contract changed from base to tree (hit), those of them at high risk,
    and how many changed code that no Spec-Unchanged spares (touched)."""
    for line in re.findall(r"^Spec-Unchanged\(([^)\n]*)\):", message, re.M):
        for name in line.split():
            if not exists(f"{tree}:sdd/modules/{name}.md"):
                batch.errors += f"ERROR Spec-Unchanged({name}): no such module. Modules: {modules(tree)}.\n"
    # The base's contracts too: a batch that deletes a high-risk contract is one to read twice.
    for contract in dict.fromkeys(contracts(tree) + contracts(base)):
        name, path = module(contract), None
        if exists(f"{tree}:{contract}"):
            paths = governs(f"{tree}:{contract}")
            if not paths:
                batch.errors += f"ERROR {contract}: governs is empty. List the paths this module owns.\n"
                continue
            broken = links(tree, contract)
            if broken:
                batch.findings += "\n".join(broken) + "\n      Fix the link, or the name of the test it points to.\n"
            path = next(iter(lines(git("diff", "--name-only", "--no-renames", base, tree, "--", *paths))), None)
        if path or contract in batch.changed:
            batch.hit.append(name)
            # The batch that drops risk: high is still judged at high risk.
            if risky(f"{tree}:{contract}") or risky(f"{base}:{contract}"):
                batch.high.append(name)
        if not path or re.search(rf"^Spec-Unchanged\({re.escape(name)}\):[^\S\n]*\S", message, re.M):
            continue
        batch.touched += 1
        if contract not in batch.changed:
            batch.findings += (
                f"DRIFT {contract}: {path} changed, its contract did not.\n"
                "      Update the contract if the code is right, fix the code if it betrays the intent,\n"
                f"      or add 'Spec-Unchanged({name}): <reason>' to the message if the behavior is unchanged.\n")


def touched(commit):
    """The modules whose code or contract a commit changes, each with its changed lines."""
    if commit_or(commit, None) is None:
        sys.exit(f"No commit {commit} here: commit first, or name a commit.")
    parent = commit_or(f"{commit}^", empty_tree())
    found = []
    for contract in contracts(commit):
        stats = git("diff", "--numstat", "--no-renames", parent, commit, "--", contract,
                    *governs(f"{commit}:{contract}"))
        changed = sum(int(row[0]) + int(row[1]) for row in (line.split("\t") for line in lines(stats)) if row[0] != "-")
        if changed:
            found.append((module(contract), changed))
    return found
