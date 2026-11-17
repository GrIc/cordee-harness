"""Drift between the contracts and their code, and the modules a commit touches."""
import re
import sys

from harness.contracts import contracts, governs, highest, in_tree, links, module, modules, risk
from harness.git import commit_or, empty_tree, git, lines


def drift(batch, base, tree, message):
    """Notes in batch the modules whose code or contract changed from base to tree (hit), the risk of each (risks),
    the contracts whose code changed (coded), the changed paths they govern (governed), and how many changed code that
    no Spec-Unchanged spares (touched)."""
    # The rule that spares a module below: one name, then a reason on its line.
    for name, reason in re.findall(r"^Spec-Unchanged\(([^)\n]*)\):(.*)", message, re.M):
        if re.search(r"\s", name):
            batch.errors += f"ERROR Spec-Unchanged({name}): name one module, one line each.\n"
        elif not in_tree(tree, f"cordee/modules/{name}.md"):
            batch.errors += f"ERROR Spec-Unchanged({name}): no such module. Modules: {modules(tree)}.\n"
        elif not reason.strip():
            batch.errors += f"ERROR Spec-Unchanged({name}): no reason. Say after the colon why the behavior holds.\n"
    owners = closest(batch.changed, base, tree,
                     {contract: governs(f"{tree}:{contract}") for contract in contracts(tree)})
    # The base's contracts too: a batch that deletes a contract is judged at its risk.
    for contract in dict.fromkeys(contracts(tree) + contracts(base)):
        name, path = module(contract), None
        if in_tree(tree, contract):
            if not governs(f"{tree}:{contract}"):
                batch.errors += f"ERROR {contract}: governs is empty. List the paths this module owns.\n"
                continue
            broken = links(tree, contract)
            if broken:
                batch.findings += "\n".join(broken) + "\n      Fix the link, or the name of the test it points to.\n"
            governed = [file for file in batch.changed if contract in owners.get(file, ())]
            batch.governed.update(governed)
            path = next(iter(governed), None)
        if path:
            batch.coded.append(contract)
        if path or contract in batch.changed:
            batch.hit.append(name)
            # The batch that lowers a module's risk is still judged at the risk it had.
            batch.risks[name] = highest(found for found in (risk(tree, contract, True), risk(base, contract, False))
                                        if found)
        if not path or re.search(rf"^Spec-Unchanged\({re.escape(name)}\):[^\S\n]*\S", message, re.M):
            continue
        batch.touched += 1
        if contract not in batch.changed:
            batch.findings += (
                f"DRIFT {contract}: {path} changed, its contract did not.\n"
                "      Update the contract if the code is right, fix the code if it betrays the intent,\n"
                f"      or add 'Spec-Unchanged({name}): <reason>' to the message if the behavior is unchanged.\n")


def closest(changed, base, tree, governed):
    """For each changed file from base to tree that a contract governs, the contracts that govern it most closely, by
    the length of the path that holds it: a module's folder inside another's is its own, a path two contracts both
    name is in both. governed maps a contract to its paths."""
    found = {}
    for contract, paths in governed.items():
        for path in paths if changed else []:
            if any(char in path for char in "*?[]:"):
                files = lines(git("diff", "--name-only", "--no-renames", base, tree, "--", path))
                depth = len(re.split(r"[*?\[:]", path)[0])
            else:
                files = [file for file in changed if file == path or file.startswith(path.rstrip("/") + "/")]
                depth = len(path.rstrip("/"))
            for file in files:
                best = found.setdefault(file, [depth, set()])
                if depth > best[0]:
                    best[:] = [depth, set()]
                if depth == best[0]:
                    best[1].add(contract)
    return {file: contracts for file, (_, contracts) in found.items()}


def touched(commit):
    """The modules whose code or contract a commit changes, each with its changed lines."""
    if commit_or(commit, None) is None:
        sys.exit(f"No commit {commit} here: commit first, or name a commit.")
    return changes(commit_or(f"{commit}^", empty_tree()), commit)


def changes(base, tree):
    """The modules whose code or contract changes from base to tree, each with its changed lines."""
    found = []
    for contract in contracts(tree):
        stats = git("diff", "--numstat", "--no-renames", base, tree, "--", contract, *governs(f"{tree}:{contract}"))
        changed = sum(int(row[0]) + int(row[1]) for row in (line.split("\t") for line in lines(stats)) if row[0] != "-")
        if changed:
            found.append((module(contract), changed))
    return found
