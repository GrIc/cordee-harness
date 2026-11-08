# Split test/run by module

Seen on 2026-11-05, when checks.md was split into checks, quiz, brief and contracts: test/run stays governed by
checks alone, so a batch that changes quiz.py, brief.py or contracts.py with its test touches two modules (a SIZE
refusal, or `Spec-Unchanged(checks)` each time).

What: move each module's tests to its own file (test/quiz, test/brief, test/contracts), governed by that module, as
test/cockpit and test/ledger are, and run them in CI.
