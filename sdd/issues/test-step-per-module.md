# A batch of tests alone lowers every module, not only the one its tests prove

What: `template/sdd/bin/fabrik/checks.py` computes the step of decision 57 once for the batch and lowers every risk in
`batch.risks` with it. A test governed by a module at `high` and linked from another module's contract takes that
batch from `high` to `normal`: one to three questions instead of three or more citing every hunk. A project whose
`sensitive` list drops `sdd/modules/` also lets a contract at `intent` move with its tests and ask no quiz.

Why: the step should come from the module whose contract links the tests, and a module whose contract the batch
changes should keep its risk.

Where: an automated security review of commit 812a574, on 2026-11-06. Not reachable with the kit's list, which keeps
`sdd/modules/` sensitive; the cross-module link is rare.
