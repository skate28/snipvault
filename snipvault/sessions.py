"""JSON-backed storage for terminal sessions.

A session records the commands you run between `snipvault start` and
`snipvault end`. Sessions live in a single JSON file (default:
~/.snipvault-sessions.json) shaped as:

    {
        "active": 3,
        "sessions": [
            {
                "id": 3,
                "name": "deploy work",
                "started": "2026-07-07T21:30:12",
                "ended": null,
                "commands": [
                    {"text": "git status", "timestamp": "2026-07-07T21:30:15"}
                ]
            }
        ]
    }

`active` is the id of the session currently recording, or null when none is.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

DEFAULT_SESSIONS = Path.home() / ".snipvault-sessions.json"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Command:
    text: str
    timestamp: str


@dataclass
class Session:
    id: int
    name: str
    started: str
    ended: str | None = None
    commands: list[Command] = field(default_factory=list)

    def duration_seconds(self) -> int | None:
        """Seconds between start and end, or None if still active."""
        if not self.ended:
            return None
        start = datetime.fromisoformat(self.started)
        end = datetime.fromisoformat(self.ended)
        return int((end - start).total_seconds())


class SessionStore:
    """Loads, saves, and queries recorded sessions in a JSON file."""

    def __init__(self, path: Path | str = DEFAULT_SESSIONS):
        self.path = Path(path)
        # A tiny marker file the shell hook checks before doing any work, so
        # there is zero overhead when no session is recording.
        self.flag_path = Path(str(self.path) + ".recording")
        self.sessions: list[Session] = []
        self.active: int | None = None
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.active = raw.get("active")
        self.sessions = [
            Session(
                id=item["id"],
                name=item["name"],
                started=item["started"],
                ended=item.get("ended"),
                commands=[Command(**c) for c in item.get("commands", [])],
            )
            for item in raw.get("sessions", [])
        ]

    def _save(self) -> None:
        payload = {
            "active": self.active,
            "sessions": [asdict(s) for s in self.sessions],
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _next_id(self) -> int:
        return max((s.id for s in self.sessions), default=0) + 1

    def active_session(self) -> Session | None:
        if self.active is None:
            return None
        for s in self.sessions:
            if s.id == self.active:
                return s
        return None

    def start(self, name: str = "") -> Session:
        if self.active_session() is not None:
            raise ValueError(
                "a session is already active; run 'snipvault end' first"
            )
        session = Session(
            id=self._next_id(),
            name=name.strip() or "session",
            started=_now(),
        )
        self.sessions.append(session)
        self.active = session.id
        self._save()
        self.flag_path.write_text(str(session.id), encoding="utf-8")
        return session

    def record(self, text: str) -> bool:
        """Append a command to the active session. No-op if none is active.

        Returns True if recorded. Kept cheap and error-free so it can run from
        a shell hook after every command.
        """
        session = self.active_session()
        if session is None or not text.strip():
            return False
        session.commands.append(Command(text=text.rstrip("\n"), timestamp=_now()))
        self._save()
        return True

    def end(self) -> Session:
        session = self.active_session()
        if session is None:
            raise ValueError("no active session; run 'snipvault start' first")
        session.ended = _now()
        self.active = None
        self._save()
        if self.flag_path.exists():
            self.flag_path.unlink()
        return session

    def get(self, session_id: int) -> Session:
        for s in self.sessions:
            if s.id == session_id:
                return s
        raise KeyError(f"no session with id {session_id}")

    def all(self) -> list[Session]:
        return list(self.sessions)
