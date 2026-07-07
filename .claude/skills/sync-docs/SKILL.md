---
name: sync-docs
description: Bring snipvault-docs.md and README.md back in sync with the actual source code - refresh the quoted source listings, usage examples, and project layout. Use after code changes, or when the user asks to update or sync the docs.
---

# Sync the documentation

`snipvault-docs.md` quotes the full source of every file, so it goes stale the
moment code changes. This skill refreshes it.

1. **Read the current source files:** `pyproject.toml`,
   `snipvault/__init__.py`, `snipvault/__main__.py`, `snipvault/storage.py`,
   `snipvault/cli.py`, `tests/test_storage.py`, `tests/test_cli.py`.

2. **Update `snipvault-docs.md`:**
   - Replace each code listing in the "Full source code" section with the
     current file contents, verbatim.
   - Update the "Usage guide" section if commands, flags, or output formats
     changed (check against `build_parser()` in `cli.py`).
   - Update the project-layout tree if files were added or removed.

3. **Update `README.md`:** usage examples and project layout only — the README
   stays short; it does not quote source code.

4. **Verify accuracy:** every command shown in the docs must match what
   `snipvault --help` and the subcommand `--help` outputs actually accept.
   Run them if unsure.

5. **Report** which sections changed and which were already in sync.

Do not change any code while running this skill — docs only.
