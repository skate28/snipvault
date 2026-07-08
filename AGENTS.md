# Snippet Vault — Agent Instructions

Tiny, dependency-free Python CLI that stores code snippets in a local JSON file.
Package: `snipvault/`. Tests: `tests/`. Full docs: `snipvault-docs.md`.

## Commands

- Run tests (do this before considering any change done): `python -m unittest discover -s tests -v`
- Reinstall after packaging changes: `python -m pip install -e .`
- Run the app: `snipvault --help` (installed) or `python -m snipvault --help`
- Website (Next.js, in `website/`): `cd website && npm run dev` (local) / `npm run build` (verify).
  The website is a separate npm project with its own `AGENTS.md` — read that before editing it.

## Distribution

- Release binaries are built by `.github/workflows/release.yml` on pushing a `v*` tag
  (PyInstaller `--onefile` per OS). Cut a release with the `/release` skill, then
  `git tag vX.Y.Z && git push origin vX.Y.Z`.
- Install scripts `install.ps1` / `install.sh` pull the latest release binary — keep the
  asset names in them in sync with the workflow's build matrix.

## Hard constraints

- Python 3.10+, **standard library only** — never add runtime dependencies.
- Tests use **unittest**, never pytest. No mocking/fixtures libraries.
- Tests must **never touch the real `~/.snipvault.json`** — always use temp vaults
  via `tempfile.TemporaryDirectory` with `addCleanup` (see existing tests).
  The same rule applies to the sessions file `~/.snipvault-sessions.json` — pass
  `--sessions <temp>` (the `run_cli` helper already does).
- The version lives in **three places** that must stay in sync:
  `pyproject.toml`, `snipvault/__init__.py`, and `website/app/lib/site.ts`.

## Architecture & conventions

- `storage.py` (snippets → `Vault`) and `sessions.py` (recorded sessions →
  `SessionStore`) are the data layers; `cli.py` is presentation (argparse +
  printing). Keep that separation — no printing from the data layers, no JSON
  handling in cli. Both stores take an injectable path for testing.
- `_record` is a hidden command called by the shell hook after each command; it
  must stay silent, fast, and never fail the shell (always exit 0).
- CLI tests call `main()` in-process through the `run_cli` helper in
  `tests/test_cli.py` — never spawn a subprocess.
- One behavior per test method; descriptive snake_case names stating the
  expected behavior (e.g. `test_show_missing_id_errors`).
- User-facing errors: raise `ValueError`/`KeyError` in storage; `cli.main`
  catches them, prints `error: ...` to stderr, returns exit code 1.

## Adding a CLI subcommand (touch all four places)

1. Parser entry in `build_parser()` in `cli.py`
2. Dispatch branch in `main()` in `cli.py`
3. CLI test(s) in `tests/test_cli.py`
4. Docs: usage sections in `README.md` and `snipvault-docs.md`

## Definition of done

- Full test suite passes (run it, don't assume).
- New behavior is covered by tests.
- Docs updated if commands or behavior changed.
