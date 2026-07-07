---
name: add-command
description: Scaffold a new snipvault CLI subcommand across all four required places - parser, dispatch, tests, and docs. Use when the user asks to add a new command or subcommand to the CLI.
---

# Add a CLI subcommand

A new subcommand must touch **four places**. Missing one is the most common
mistake in this repo — verify all four before finishing.

1. **Parser** — in `snipvault/cli.py`, `build_parser()`: add a
   `sub.add_parser("<name>", help="...")` entry with its arguments, following
   the style of the existing `add`/`show`/`search` parsers.

2. **Dispatch** — in `snipvault/cli.py`, `main()`: add an
   `elif args.command == "<name>":` branch. Keep logic in `snipvault/storage.py`
   (add a `Vault` method if needed); the branch should only call storage and print.
   Errors: raise `ValueError`/`KeyError` in storage — `main()` already converts
   them to `error: ...` on stderr with exit code 1.

3. **Tests** — in `tests/test_cli.py`: at least one happy-path test and one
   error-path test through the `run_cli` helper (in-process, never subprocess).
   If you added a `Vault` method, unit-test it in `tests/test_storage.py` too,
   using the temp-vault `setUp` pattern.

4. **Docs** — add the command to the usage sections of `README.md` and
   `snipvault-docs.md` (and update the source listings in `snipvault-docs.md`
   if you changed files that are quoted there — or run the `sync-docs` skill).

Finish by running the full suite and reporting results:

```
python -m unittest discover -s tests -v
```

Constraints: standard library only; unittest only; storage stays
presentation-free (no printing in `storage.py`).
