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

Constraints: as [checks](checks.md).
