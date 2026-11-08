# Tokens: what agents spend

Optional (`tokens: true` in `cordee/config.yml`, then `bash cordee/bin/cordee install-hook`). `cordee/bin/ledger` keeps
what agents spent on each module, by month, in the git notes `cordee-ledger`: the cost of the product's features, with
no commit, author or date. The hooks `install-hook` writes note it at each commit and share it at each push, unless the
dev sets `git config cordee.ledger false` (`--global` for every repo). The tokens come from `cordee/bin/cockpit`, which
reads the agents' logs on this machine, Claude Code's, opencode's and Kilo Code's. `bash cordee/bin/cockpit report
"$PWD"`, from any folder of the repo, shows a dev where their own tokens went; `bash cordee/bin/cockpit hints` says
what to cut, or which module's quizzes the dev flagged, once in 10 batches at most. To audit a clone, `git fetch origin
refs/notes/cordee-ledger:refs/notes/cordee-ledger`, then `bash cordee/bin/ledger report`: the tokens by month, module,
role and model, then per month the batches noted against the agent commits.
