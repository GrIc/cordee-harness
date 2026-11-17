# Learn a module (for agents)

When the dev takes over code they did not write, a quiz on a module no batch changes, graded without a commit. It
lives in `LEARN.md` and its own key, so a batch's `QUIZ.md` can wait beside it.

1. Without `cordee/modules/<module>.md`, write the contract from the code and its tests, as the workflow's Contracts
   says: `governs`, the intent the code and tests show, criteria linked to the tests that prove them. Ask the dev what
   the code leaves open, and add the module to the map in `cordee/README.md`. It is read from the disk: the dev may
   learn the module before committing it.
2. Run `bash cordee/bin/cordee learn <module>`. It prints the fingerprint line, `learn <module> <commit>`, and the
   two paths to write.
3. Spawn a fresh reviewer, as in step 6 of COMPILE, in the dev's language. It reads the contract, the code and its
   tests, and writes `LEARN.md` in the form of a batch's quiz: one to three questions on what the module does and why,
   the promise of its contract, the options its decisions rejected. Each `See` line cites the files the module governs
   or the tests its contract links. It sends the key, the fingerprint line then one line per question as for a batch,
   to `bash cordee/bin/cordee learn --key` on its standard input, and runs `bash cordee/bin/cordee learn --audit`
   until it passes. It reports how many questions it wrote and what the audit printed, never a right box.
4. The dev ticks the boxes and runs `bash cordee/bin/cordee learn --grade`. A wrong answer gets its hint and the boxes
   to say why, as in a batch's quiz; when the dev types *quiz feedback*, read `LEARN.md` as the block in `AGENTS.md`
   says of `QUIZ.md`. Once all are right, the questions the dev flagged go to the quiz journal on that module, and
   `LEARN.md` and its key are deleted.

Once HEAD moves, `See` lines point at the code as it was when the quiz was written: grading only warns.
