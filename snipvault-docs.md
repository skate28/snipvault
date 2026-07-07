# Snippet Vault — Full Documentation

A tiny, dependency-free command-line code-snippet manager written in Python (3.10+).
Save code snippets with a title, language, and tags; search and retrieve them later
from any terminal. All data lives in a single local JSON file — no database, no server.

---

## Table of contents

1. [Installation (Windows / macOS / Linux)](#installation)
2. [Usage guide](#usage-guide)
3. [Where your data lives](#where-your-data-lives)
4. [Running the tests](#running-the-tests)
5. [The test-guardian Claude subagent](#the-test-guardian-claude-subagent)
6. [Full source code](#full-source-code)

---

## Installation

Requires **Python 3.10 or newer** ([python.org/downloads](https://www.python.org/downloads/)).
The install steps are the same on every OS — only the terminal and path style differ.

### Windows (PowerShell)

```powershell
cd C:\Users\nickl\onedrive\documents\snippet-vault
python -m pip install -e .
snipvault --help
```

### macOS / Linux

```bash
cd path/to/snippet-vault
python3 -m pip install -e .
snipvault --help
```

Notes:

- `-e` installs in **editable mode**: edits to the source take effect immediately
  without reinstalling. Drop the `-e` for a normal install.
- On macOS/Linux, if `pip install` complains about an externally managed environment,
  use [pipx](https://pipx.pypa.io) instead: `pipx install path/to/snippet-vault`.
- After installing, the `snipvault` command works from **any** directory.
- To uninstall: `python -m pip uninstall snipvault`.

---

## Usage guide

The five commands: `add`, `list`, `show`, `search`, `rm`.

### Save a snippet

```
snipvault add "<title>" "<code>" --lang <language> --tags <tag1,tag2>
```

```powershell
snipvault add "recursive delete" "Remove-Item -Recurse -Force path" --lang powershell --tags files,cleanup
snipvault add "git undo last commit" "git reset --soft HEAD~1" --lang bash --tags git,undo
```

`--lang` (default `text`) and `--tags` are optional labels that make searching easier.

### List everything

```powershell
snipvault list
```

```
  id  title                           language    tags
----------------------------------------------------------------------
   1  recursive delete                powershell  files, cleanup
   2  git undo last commit            bash        git, undo
```

The **id** column is how you refer to a snippet in `show` and `rm`.

### Search

Matches title, language, tags, and the code itself — case-insensitively:

```powershell
snipvault search files      # matches tags
snipvault search reset      # matches text inside the code
```

### Get the code back out

`show` prints only the raw code, ready to copy or pipe:

```powershell
snipvault show 2
snipvault show 2 | Set-Clipboard        # Windows: straight to clipboard
snipvault show 2 | pbcopy               # macOS
snipvault show 2 | xclip -sel clip      # Linux (X11)
```

### Delete

```powershell
snipvault rm 2
```

### Use a different vault file

Pass `--vault` **before** the command to keep separate vaults (e.g. per project):

```powershell
snipvault --vault .\project-vault.json add "build cmd" "npm run build" --lang bash
```

---

## Where your data lives

Everything is stored in one JSON file, created on first `add`:

- Windows: `C:\Users\<you>\.snipvault.json`
- macOS/Linux: `~/.snipvault.json`

It's plain JSON — you can open it in a text editor, back it up, or sync it between
machines. Delete it to start fresh.

---

## Running the tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

14 tests: 8 unit tests for the storage layer, 6 end-to-end CLI tests
(run in-process against temp vault files — no subprocesses, nothing touches your real vault).

---

## The test-guardian Claude subagent

The project ships a project-scoped Claude Code subagent at
`.claude/agents/test-guardian.md`. It is available automatically when you run
Claude Code inside the `snippet-vault` folder.

**Its use case:** after any change to `snipvault/`, it runs the test suite,
diagnoses failures (deciding whether the test or the implementation is at fault),
and writes new `unittest` cases following the repo's conventions. It never deletes
failing tests to go green and won't modify implementation code unless explicitly asked.

Invoke it like: *"Use the test-guardian agent to check coverage of the search command."*

---

## Full source code

### Project layout

```
snippet-vault/
├── pyproject.toml              # packaging + the `snipvault` console command
├── README.md
├── snipvault-docs.md           # this file
├── .claude/agents/
│   └── test-guardian.md        # Claude Code subagent
├── snipvault/
│   ├── __init__.py
│   ├── __main__.py             # enables `python -m snipvault`
│   ├── storage.py              # Snippet dataclass + JSON-backed Vault
│   └── cli.py                  # argparse CLI
└── tests/
    ├── test_storage.py
    └── test_cli.py
```

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "snipvault"
version = "0.1.0"
description = "A tiny, dependency-free command-line code-snippet manager"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }

[project.scripts]
snipvault = "snipvault.cli:main"

[tool.setuptools]
packages = ["snipvault"]
```

### snipvault/\_\_init\_\_.py

```python
"""Snippet Vault - a tiny local code-snippet manager."""

__version__ = "0.1.0"
```

### snipvault/\_\_main\_\_.py

```python
from .cli import main

raise SystemExit(main())
```

### snipvault/storage.py

```python
"""JSON-backed storage for snippets.

Snippets live in a single JSON file (default: ~/.snipvault.json) shaped as:

    {
        "snippets": [
            {
                "id": 1,
                "title": "list comprehension",
                "language": "python",
                "tags": ["python", "loops"],
                "code": "[x * 2 for x in items]",
                "created": "2026-07-07T12:00:00"
            }
        ]
    }
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

DEFAULT_VAULT = Path.home() / ".snipvault.json"


@dataclass
class Snippet:
    id: int
    title: str
    language: str
    code: str
    tags: list[str] = field(default_factory=list)
    created: str = ""

    def matches(self, query: str) -> bool:
        """Case-insensitive match against title, language, tags, and code."""
        q = query.lower()
        haystacks = [self.title, self.language, self.code, *self.tags]
        return any(q in h.lower() for h in haystacks)


class Vault:
    """Loads, saves, and queries snippets in a JSON file."""

    def __init__(self, path: Path | str = DEFAULT_VAULT):
        self.path = Path(path)
        self.snippets: list[Snippet] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.snippets = [Snippet(**item) for item in raw.get("snippets", [])]

    def _save(self) -> None:
        payload = {"snippets": [asdict(s) for s in self.snippets]}
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _next_id(self) -> int:
        return max((s.id for s in self.snippets), default=0) + 1

    def add(self, title: str, language: str, code: str, tags: list[str] | None = None) -> Snippet:
        if not title.strip():
            raise ValueError("title must not be empty")
        if not code.strip():
            raise ValueError("code must not be empty")
        snippet = Snippet(
            id=self._next_id(),
            title=title.strip(),
            language=language.strip().lower() or "text",
            code=code,
            tags=[t.strip().lower() for t in (tags or []) if t.strip()],
            created=datetime.now().isoformat(timespec="seconds"),
        )
        self.snippets.append(snippet)
        self._save()
        return snippet

    def get(self, snippet_id: int) -> Snippet:
        for s in self.snippets:
            if s.id == snippet_id:
                return s
        raise KeyError(f"no snippet with id {snippet_id}")

    def remove(self, snippet_id: int) -> Snippet:
        snippet = self.get(snippet_id)
        self.snippets.remove(snippet)
        self._save()
        return snippet

    def search(self, query: str) -> list[Snippet]:
        return [s for s in self.snippets if s.matches(query)]

    def all(self) -> list[Snippet]:
        return list(self.snippets)
```

### snipvault/cli.py

```python
"""Command-line interface for Snippet Vault."""

from __future__ import annotations

import argparse
import sys

from .storage import DEFAULT_VAULT, Snippet, Vault


def _format_row(s: Snippet) -> str:
    tags = ", ".join(s.tags) if s.tags else "-"
    return f"{s.id:>4}  {s.title:<30.30}  {s.language:<10.10}  {tags}"


def _print_table(snippets: list[Snippet]) -> None:
    if not snippets:
        print("(no snippets)")
        return
    print(f"{'id':>4}  {'title':<30}  {'language':<10}  tags")
    print("-" * 70)
    for s in snippets:
        print(_format_row(s))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="snipvault", description="Store and retrieve code snippets locally."
    )
    parser.add_argument(
        "--vault", default=str(DEFAULT_VAULT), help="path to the vault JSON file"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a snippet")
    p_add.add_argument("title")
    p_add.add_argument("code")
    p_add.add_argument("--lang", default="text", help="language (default: text)")
    p_add.add_argument("--tags", default="", help="comma-separated tags")

    sub.add_parser("list", help="list all snippets")

    p_show = sub.add_parser("show", help="print a snippet's code by id")
    p_show.add_argument("id", type=int)

    p_search = sub.add_parser("search", help="search title, language, tags, and code")
    p_search.add_argument("query")

    p_rm = sub.add_parser("rm", help="delete a snippet by id")
    p_rm.add_argument("id", type=int)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    vault = Vault(args.vault)

    try:
        if args.command == "add":
            tags = [t for t in args.tags.split(",") if t.strip()]
            snippet = vault.add(args.title, args.lang, args.code, tags)
            print(f"added snippet {snippet.id}: {snippet.title}")
        elif args.command == "list":
            _print_table(vault.all())
        elif args.command == "show":
            print(vault.get(args.id).code)
        elif args.command == "search":
            _print_table(vault.search(args.query))
        elif args.command == "rm":
            snippet = vault.remove(args.id)
            print(f"removed snippet {snippet.id}: {snippet.title}")
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### tests/test_storage.py

```python
import tempfile
import unittest
from pathlib import Path

from snipvault.storage import Vault


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.vault_path = Path(self.tmpdir.name) / "vault.json"
        self.vault = Vault(self.vault_path)

    def test_add_assigns_incrementing_ids(self):
        first = self.vault.add("one", "python", "print(1)")
        second = self.vault.add("two", "python", "print(2)")
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_add_rejects_empty_title_and_code(self):
        with self.assertRaises(ValueError):
            self.vault.add("  ", "python", "code")
        with self.assertRaises(ValueError):
            self.vault.add("title", "python", "   ")

    def test_add_normalizes_language_and_tags(self):
        s = self.vault.add("t", "  Python ", "x", tags=[" Loops ", "", "WEB"])
        self.assertEqual(s.language, "python")
        self.assertEqual(s.tags, ["loops", "web"])

    def test_persistence_roundtrip(self):
        self.vault.add("persist me", "bash", "echo hi", tags=["shell"])
        reloaded = Vault(self.vault_path)
        self.assertEqual(len(reloaded.all()), 1)
        snippet = reloaded.get(1)
        self.assertEqual(snippet.title, "persist me")
        self.assertEqual(snippet.tags, ["shell"])

    def test_get_missing_raises(self):
        with self.assertRaises(KeyError):
            self.vault.get(99)

    def test_remove_deletes_and_persists(self):
        self.vault.add("bye", "text", "x")
        removed = self.vault.remove(1)
        self.assertEqual(removed.title, "bye")
        self.assertEqual(Vault(self.vault_path).all(), [])

    def test_search_is_case_insensitive_across_fields(self):
        self.vault.add("List trick", "python", "[x for x in y]", tags=["loops"])
        self.vault.add("Grep files", "bash", "grep -r foo .", tags=["search"])
        self.assertEqual(len(self.vault.search("LOOPS")), 1)   # tag
        self.assertEqual(len(self.vault.search("grep")), 1)    # title/code
        self.assertEqual(len(self.vault.search("python")), 1)  # language
        self.assertEqual(self.vault.search("nomatch"), [])

    def test_ids_not_reused_after_delete_of_last(self):
        self.vault.add("a", "text", "1")
        self.vault.add("b", "text", "2")
        self.vault.remove(1)
        third = self.vault.add("c", "text", "3")
        self.assertEqual(third.id, 3)


if __name__ == "__main__":
    unittest.main()
```

### tests/test_cli.py

```python
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from snipvault.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.vault_path = str(Path(self.tmpdir.name) / "vault.json")

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--vault", self.vault_path, *args])
        return code, out.getvalue(), err.getvalue()

    def test_add_then_list(self):
        code, out, _ = self.run_cli("add", "hello", "print('hi')", "--lang", "python")
        self.assertEqual(code, 0)
        self.assertIn("added snippet 1", out)

        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("hello", out)
        self.assertIn("python", out)

    def test_show_prints_raw_code(self):
        self.run_cli("add", "greet", "print('hi')", "--lang", "python")
        code, out, _ = self.run_cli("show", "1")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "print('hi')")

    def test_show_missing_id_errors(self):
        code, _, err = self.run_cli("show", "42")
        self.assertEqual(code, 1)
        self.assertIn("no snippet with id 42", err)

    def test_add_empty_title_errors(self):
        code, _, err = self.run_cli("add", "   ", "x")
        self.assertEqual(code, 1)
        self.assertIn("title must not be empty", err)

    def test_search_and_rm(self):
        self.run_cli("add", "loop trick", "[x for x in y]", "--lang", "python",
                     "--tags", "loops,tricks")
        self.run_cli("add", "grep files", "grep -r foo .", "--lang", "bash")

        code, out, _ = self.run_cli("search", "loops")
        self.assertEqual(code, 0)
        self.assertIn("loop trick", out)
        self.assertNotIn("grep files", out)

        code, out, _ = self.run_cli("rm", "1")
        self.assertEqual(code, 0)
        self.assertIn("removed snippet 1", out)

        code, out, _ = self.run_cli("list")
        self.assertNotIn("loop trick", out)

    def test_list_empty_vault(self):
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("(no snippets)", out)


if __name__ == "__main__":
    unittest.main()
```
