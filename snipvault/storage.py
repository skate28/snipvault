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
