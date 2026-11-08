# A script that imports harness leaves __pycache__ in template/

Seen on 2026-11-08: a reviewer's probe imported `harness` without `-B`, and `git add -A` staged its `.pyc` files with
the batch. The launchers run Python with `-B` and write none, but the kit's `.gitignore` does not list `__pycache__/`.

What: add `__pycache__/` to the kit's `.gitignore` (not the template's: a deployed repo has its own).
