# Kilo Code may read like opencode

Seen on 2026-11-05 in Kilo's documentation: Kilo Code is built on opencode, reads `kilo.jsonc` and the legacy
`opencode.json`, and its VS Code extension shares the CLI's config. Its logs may be opencode's SQLite base under
another folder, so its reader could be the opencode one with another path.

Teams start with Kilo Code and Copilot as VS Code extensions on 2026-11-09: their ledger stays empty until then.

Where: `template/sdd/bin/fabrik/logs/`, the roadmap line on Kilo Code and Copilot in the cockpit.
