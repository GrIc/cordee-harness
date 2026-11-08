# The ledger finds no opencode session on Windows

Seen on 2026-11-05 in the first field use (opencode and Qwen, Windows, Git Bash): after three agent commits,
`.git/sdd/ledger-until` moved to the last one but `refs/notes/sdd-ledger` does not exist, so `cockpit usage` returned
nothing each time.

Guess, to check against the owner's export of the session table: the reader keeps a session when
`session.directory = repo`, where `repo` comes from `git rev-parse --show-toplevel` (`C:/Users/...`), while opencode
stores the directory Windows writes (`C:\Users\...`), maybe in another case. A session started in a worktree would
miss too.

Kilo Code reads through the same `read()` since 2026-11-08: the fix covers both.

Where: `template/sdd/bin/fabrik/logs/opencode.py`, `test/cockpit`.
