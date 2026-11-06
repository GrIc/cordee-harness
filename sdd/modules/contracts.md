---
governs: [template/sdd/bin/fabrik/contracts.py]
depends: [checks]
---
# contracts

How the script reads a contract, written as the workflow's Contracts section says.

- `governs` lists git pathspecs, as a list in brackets that may wrap, as `- path` lines below the key, or as one path;
  the next key and comments are no paths: [test_governs_takes_git_pathspecs](/test/run),
  [test_multiline_governs_is_read_fully](/test/run), [test_governs_reads_a_scalar_or_a_block_list](/test/run). An
  absolute path or one outside the repo stops every command that reads it, naming the contract and what to do:
  [test_a_governs_path_outside_the_repo_says_what_to_do](/test/run).
- A link in a contract, written as the workflow says, even wrapped over two lines or with an anchor, is drift when the
  commit lacks its file, or when its text is neither found as whole words in that file nor its name or path. Web links
  and links to markdown or to a directory are not checked: [test_a_link_to_a_missing_file_is_drift](/test/run),
  [test_a_link_to_a_missing_test_name_is_drift](/test/run),
  [test_audit_accepts_links_to_names_groups_and_files](/test/run), also in a worktree's hook:
  [test_a_worktree_hook_reads_relative_links](/test/run).
- A setting is read from the contract's front matter, else from `sdd/config.yml`, else the kit's default; both hold
  flat `key: value` lines, with quotes and comments allowed. `risk: high` in `sdd/config.yml` puts every module that
  does not say otherwise at high risk, and a contract's `risk: normal` keeps it at normal risk; without the file, the
  harness behaves as before: [test_the_config_sets_the_risk_a_contract_overrides](/test/run).
- `risk` takes `low`, `intent`, `normal` or `high`, in lower case. Another value stops the commit with an ERROR that
  names its file and lists the four; in the base it counts as `normal`, so that the commit fixing it passes:
  [test_a_risk_is_one_of_four_values](/test/run).

Constraints: as [checks](checks.md).
