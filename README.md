# Snippet Vault

A tiny, dependency-free command-line code-snippet manager in Python (3.10+).
Snippets are stored in a single JSON file (default `~/.snipvault.json`).

## Install

No Python required — the installers download a single self-contained binary.

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/skate28/snipvault/main/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/skate28/snipvault/main/install.sh | sh
```

Or download a binary directly from the [latest release](https://github.com/skate28/snipvault/releases/latest),
or install from source with pip:
```bash
pip install git+https://github.com/skate28/snipvault.git
```

### Uninstall

**Windows:** `irm https://raw.githubusercontent.com/skate28/snipvault/main/uninstall.ps1 | iex`
**macOS / Linux:** `curl -fsSL https://raw.githubusercontent.com/skate28/snipvault/main/uninstall.sh | sh`

These remove the binary and PATH entry but **leave your saved snippets** at
`~/.snipvault.json`. Delete that file yourself if you also want to erase your data.
(If you installed with pip instead: `pip uninstall snipvault`.)

## Usage

Run `snipvault help` (or just `snipvault` with no arguments) any time to see all commands.

```
python -m snipvault add "list comprehension" "[x*2 for x in items]" --lang python --tags loops,python
python -m snipvault list
python -m snipvault search loops
python -m snipvault show 1
python -m snipvault rm 1
```

Use `--vault path\to\file.json` before the command to point at a different vault file
(handy for testing or keeping vaults per project).

## Project layout

```
snippet-vault/
├── AGENTS.md             # cross-tool agent instructions (Claude Code, Cursor, ...)
├── CLAUDE.md             # one-line shim importing AGENTS.md
├── pyproject.toml        # packaging + the `snipvault` console command
├── install.ps1           # Windows one-line installer
├── install.sh            # macOS/Linux one-line installer
├── snipvault/
│   ├── storage.py        # Snippet dataclass + JSON-backed Vault
│   ├── cli.py            # argparse CLI (add / list / show / search / rm)
│   └── __main__.py       # enables `python -m snipvault`
├── packaging/entry.py    # PyInstaller entry point for release binaries
├── website/              # Next.js landing page (deployed to Vercel)
├── tests/
│   ├── test_storage.py   # Vault unit tests
│   └── test_cli.py       # end-to-end CLI tests (in-process, no subprocess)
├── .github/workflows/    # CI tests + tag-triggered release binary builds
├── .githooks/
│   └── pre-commit        # runs the test suite before every commit
└── .claude/
    ├── agents/test-guardian.md      # test-engineer subagent (see below)
    ├── skills/                      # portable SKILL.md workflows:
    │   ├── release/                 #   /release — version bump + test + reinstall
    │   ├── add-command/             #   /add-command — scaffold a CLI subcommand
    │   └── sync-docs/               #   /sync-docs — refresh snipvault-docs.md
    ├── hooks/protect_vault.py       # blocks agent access to ~/.snipvault.json
    └── settings.json                # wires the protect_vault hook
```

New clones must enable the shared git hooks once:

```
git config core.hooksPath .githooks
```

## Running tests

```
python -m unittest discover -s tests -v
```

## The `test-guardian` subagent

This project ships a Claude Code subagent in `.claude/agents/test-guardian.md`.
Its specific use case: whenever code in `snipvault/` changes, it runs the test
suite, diagnoses failures, and writes new `unittest` cases for uncovered
behavior — following this repo's conventions (temp vaults, in-process CLI
calls, stdlib only). Invoke it from Claude Code in this folder, e.g.:

> "Use the test-guardian agent to check coverage of the search command."
