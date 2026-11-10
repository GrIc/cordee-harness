# The tokens setting in config.yml is never validated

Seen on 2026-11-09 during review: `hooks.tokens_on()` tests `value(text, "tokens") == "true"`. If a developer writes
`tokens: yes`, `tokens: True`, or `tokens: on` in `cordee/config.yml`, it is silently evaluated as `false` with no feedback.

Why: All other settings in `cordee/config.yml` (`risk`, `batch-lines`, `review-wait-hours`, `abandoned-days`, `sensitive`,
`not-code`, `agent-emails`) validate their inputs and stop with `ERROR cordee/config.yml: ...`.

Leads:
- Validate `tokens` in `hooks.tokens_on()` or `contracts.py`, exiting with an `ERROR` if the value is not `true` or `false`
  when set.

Where: `template/cordee/bin/harness/hooks.py` (`tokens_on`), `template/cordee/bin/harness/contracts.py`.
