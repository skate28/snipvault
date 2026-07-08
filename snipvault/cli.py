"""Command-line interface for Snippet Vault."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from .sessions import DEFAULT_SESSIONS, Session, SessionStore
from .storage import DEFAULT_VAULT, Snippet, Vault


def parse_tags(raw: list[str] | None) -> list[str]:
    """Turn whatever the shell passed to --tags into a clean tag list.

    Accepts commas, spaces, or both: `--tags a,b,c`, `--tags a b c`, and
    `--tags "a, b, c"` all yield ["a", "b", "c"].
    """
    if not raw:
        return []
    return [t for t in re.split(r"[,\s]+", " ".join(raw)) if t]

# (command, one-line description, example of exactly what to type)
COMMANDS = [
    ("add", "Save a snippet", 'snipvault add "title" "code here" --lang python --tags tag1,tag2'),
    ("list", "List all your snippets", "snipvault list"),
    ("search", "Search titles, languages, tags, and code", "snipvault search keyword"),
    ("show", "Print a snippet's code by its id", "snipvault show 1"),
    ("rm", "Delete a snippet by its id", "snipvault rm 1"),
    ("start", "Start recording a terminal session", 'snipvault start "deploy work"'),
    ("end", "Stop recording the active session", "snipvault end"),
    ("sessions", "List your recorded sessions", "snipvault sessions"),
    ("sessions rm", "Delete a recorded session by its id", "snipvault sessions rm 1"),
    ("session", "Show a session's command log by id", "snipvault session 1"),
    ("init", "Set up shell recording (run once)", "snipvault init"),
    ("uninstall", "Show how to remove Snippet Vault", "snipvault uninstall"),
    ("help", "Show this help message", "snipvault help"),
]

_RAW = "https://raw.githubusercontent.com/skate28/snipvault/main"


def print_uninstall_help() -> None:
    """Print the command to fully remove Snippet Vault for the current OS.

    A running binary can't reliably delete itself (on Windows the .exe is
    locked while executing), so we show the exact one-liner to run instead.
    """
    print("To uninstall Snippet Vault, run:\n")
    if sys.platform == "win32":
        print(f"  irm {_RAW}/uninstall.ps1 | iex")
    else:
        print(f"  curl -fsSL {_RAW}/uninstall.sh | sh")
    print()
    print("That removes the snipvault program and its PATH entry, but KEEPS your")
    print("saved snippets so you can reinstall later without losing them.")
    print()
    print("Your snippets are stored in this one file:")
    print(f"  {DEFAULT_VAULT}")
    print("If you also want to erase your snippets, delete that file manually:")
    if sys.platform == "win32":
        print(f'  Remove-Item "{DEFAULT_VAULT}"')
    else:
        print(f'  rm "{DEFAULT_VAULT}"')
    print()
    print("(If you installed with pip instead: pip uninstall snipvault)")


def print_help() -> None:
    """Print a friendly command list with a copy-paste example for each."""
    print("snipvault - store and retrieve code snippets locally\n")
    print("Usage: snipvault <command> [options]\n")
    print("Commands:")
    width = max(len(name) for name, _, _ in COMMANDS)
    for name, desc, example in COMMANDS:
        print(f"  {name:<{width}}  {desc}")
        print(f"  {'':<{width}}  $ {example}")
    print()
    print("Notes:")
    print("  --lang and --tags are optional.")
    print("  Tags can be separated by spaces OR commas - all of these work:")
    print("    --tags web api db")
    print("    --tags web,api,db")
    print('    --tags "web, api, db"')
    print("  Add --vault <path> before any command to use a different vault file.")


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


def _fmt_duration(seconds: int | None) -> str:
    if seconds is None:
        return "active"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def _print_sessions(sessions: list[Session]) -> None:
    if not sessions:
        print("(no sessions yet - run 'snipvault start' to record one)")
        return
    print(f"{'id':>4}  {'name':<24}  {'started':<19}  {'duration':>9}  cmds")
    print("-" * 74)
    for s in sessions:
        started = s.started.replace("T", " ")
        dur = _fmt_duration(s.duration_seconds())
        print(f"{s.id:>4}  {s.name:<24.24}  {started:<19}  {dur:>9}  {len(s.commands)}")


def _print_session(s: Session) -> None:
    print(f'Session: "{s.name}"  (id {s.id})')
    print(f"Started: {s.started.replace('T', ' ')}")
    if s.ended:
        print(f"Ended:   {s.ended.replace('T', ' ')}   ({_fmt_duration(s.duration_seconds())})")
    else:
        print("Ended:   (still recording)")
    print()
    if not s.commands:
        print("  (no commands recorded)")
        return
    for c in s.commands:
        if c.timestamp:
            clock = c.timestamp.split("T")[-1]
            print(f"  {clock}  {c.text}")
        else:
            print(f"  {c.text}")


def _shell_hook(shell: str, flag_path: str) -> str:
    """Return the recording hook script for the given shell.

    The hook only does work while a session is active (the flag file exists),
    and never records snipvault's own commands.
    """
    if shell == "powershell":
        return f'''# snipvault session recording hook
$global:__snipvault_flag = "{flag_path}"
if (-not $global:__snipvault_orig_prompt) {{
    $global:__snipvault_orig_prompt = $function:prompt
}}
$global:__snipvault_last = -1
function global:prompt {{
    if (Test-Path $global:__snipvault_flag) {{
        $h = Get-History -Count 1
        if ($h -and $h.Id -ne $global:__snipvault_last) {{
            $global:__snipvault_last = $h.Id
            $line = $h.CommandLine
            if ($line -and -not $line.StartsWith("snipvault")) {{
                snipvault _record "$line" | Out-Null
            }}
        }}
    }}
    & $global:__snipvault_orig_prompt
}}'''
    if shell == "bash":
        return f'''# snipvault session recording hook
__snipvault_flag="{flag_path}"
__snipvault_record() {{
    [ -f "$__snipvault_flag" ] || return
    local line
    line=$(history 1 | sed 's/^ *[0-9]* *//')
    case "$line" in snipvault*) return;; esac
    snipvault _record "$line" >/dev/null 2>&1
}}
case "$PROMPT_COMMAND" in
    *__snipvault_record*) ;;
    *) PROMPT_COMMAND="__snipvault_record;${{PROMPT_COMMAND}}" ;;
esac'''
    # zsh
    return f'''# snipvault session recording hook
__snipvault_flag="{flag_path}"
__snipvault_record() {{
    [ -f "$__snipvault_flag" ] || return
    local line="${{1%%$'\\n'}}"
    case "$line" in snipvault*) return;; esac
    snipvault _record "$line" >/dev/null 2>&1
}}
autoload -Uz add-zsh-hook 2>/dev/null
add-zsh-hook preexec __snipvault_record 2>/dev/null'''


def _detect_shell() -> str:
    if sys.platform == "win32":
        return "powershell"
    return "zsh" if os.environ.get("SHELL", "").endswith("zsh") else "bash"


def print_init(shell: str | None, flag_path: str) -> None:
    """Print the one-time setup for shell recording.

    With an explicit shell, print the raw hook script (for a profile to eval).
    Without one, print friendly instructions for the detected shell.
    """
    if shell:
        print(_shell_hook(shell, flag_path))
        return

    detected = _detect_shell()
    print("Set up Snippet Vault session recording (one-time):\n")
    if detected == "powershell":
        print("  Add this line to your PowerShell profile ($PROFILE):\n")
        print("    Invoke-Expression (& snipvault init powershell | Out-String)\n")
        print("  Open the profile with:  notepad $PROFILE")
    elif detected == "zsh":
        print("  Add this line to ~/.zshrc:\n")
        print('    eval "$(snipvault init zsh)"\n')
    else:
        print("  Add this line to ~/.bashrc:\n")
        print('    eval "$(snipvault init bash)"\n')
    print("Then open a NEW terminal. After that, use:")
    print('  snipvault start "my task"   # begin recording')
    print("  snipvault end               # stop and save")
    print("\nRecording only happens between start and end - nothing is captured otherwise.")


def _history_path():
    """Path to the shell history file we read for zero-setup capture.

    Overridable via SNIPVAULT_HISTORY_FILE (used in tests). On Windows this is
    the PSReadLine history file, which PowerShell updates after every command.
    """
    override = os.environ.get("SNIPVAULT_HISTORY_FILE")
    if override:
        return Path(override)
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return (
                Path(appdata)
                / "Microsoft"
                / "Windows"
                / "PowerShell"
                / "PSReadLine"
                / "ConsoleHost_history.txt"
            )
    return None


def _history_line_count() -> int | None:
    p = _history_path()
    if p and p.exists():
        return len(p.read_text(encoding="utf-8", errors="ignore").splitlines())
    return None


def _history_commands_since(marker: int | None) -> list[str]:
    """Commands added to the history file since `marker`, minus snipvault's own."""
    p = _history_path()
    if p is None or not p.exists() or marker is None:
        return []
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    new = lines[marker:]
    return [
        line for line in new
        if line.strip() and not line.strip().startswith("snipvault")
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="snipvault", description="Store and retrieve code snippets locally."
    )
    parser.add_argument(
        "--vault", default=str(DEFAULT_VAULT), help="path to the vault JSON file"
    )
    parser.add_argument(
        "--sessions",
        default=str(DEFAULT_SESSIONS),
        help="path to the sessions JSON file",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("help", help="show this help message")

    p_add = sub.add_parser("add", help="add a snippet")
    p_add.add_argument("title")
    p_add.add_argument("code")
    p_add.add_argument("--lang", default="text", help="language (default: text)")
    p_add.add_argument(
        "--tags",
        nargs="*",
        default=None,
        help="tags separated by commas or spaces, e.g. --tags web api",
    )

    sub.add_parser("list", help="list all snippets")

    p_show = sub.add_parser("show", help="print a snippet's code by id")
    p_show.add_argument("id", type=int)

    p_search = sub.add_parser("search", help="search title, language, tags, and code")
    p_search.add_argument("query")

    p_rm = sub.add_parser("rm", help="delete a snippet by id")
    p_rm.add_argument("id", type=int)

    p_start = sub.add_parser("start", help="start recording a terminal session")
    p_start.add_argument("name", nargs="?", default="", help="optional session name")

    sub.add_parser("end", help="stop recording the active session")

    p_sessions = sub.add_parser("sessions", help="list or remove recorded sessions")
    p_sessions.add_argument(
        "action", nargs="?", choices=["rm"], help="'rm' to delete a session"
    )
    p_sessions.add_argument("id", nargs="?", type=int, help="session id to remove")

    p_session = sub.add_parser("session", help="show a session's command log by id")
    # Accept both `session <id>` (show) and `session rm <id>` (delete).
    p_session.add_argument("id", help="session id, or 'rm' to delete")
    p_session.add_argument("extra", nargs="?", help="session id when using 'rm'")

    p_init = sub.add_parser("init", help="set up shell recording")
    p_init.add_argument(
        "shell",
        nargs="?",
        choices=["powershell", "bash", "zsh"],
        help="print the raw hook for this shell (used by your profile)",
    )

    p_record = sub.add_parser("_record", help=argparse.SUPPRESS)
    p_record.add_argument("text", nargs=argparse.REMAINDER)

    sub.add_parser("uninstall", help="show how to remove Snippet Vault")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Bare `snipvault` or `snipvault help` prints the full command list.
    if args.command is None or args.command == "help":
        print_help()
        return 0

    if args.command == "uninstall":
        print_uninstall_help()
        return 0

    if args.command == "init":
        store = SessionStore(args.sessions)
        print_init(args.shell, str(store.flag_path))
        return 0

    # Hidden command the shell hook calls after each command. Must be silent,
    # fast, and never fail the shell (always exit 0).
    if args.command == "_record":
        try:
            SessionStore(args.sessions).record(" ".join(args.text))
        except Exception:
            pass
        return 0

    if args.command in ("start", "end", "sessions", "session"):
        sessions = SessionStore(args.sessions)
        try:
            if args.command == "start":
                s = sessions.start(args.name, marker=_history_line_count())
                print(f'started session {s.id}: "{s.name}" (recording)')
            elif args.command == "end":
                active = sessions.active_session()
                # If nothing was recorded live (no shell hook), backfill the
                # commands from the shell history file.
                if active is not None and not active.commands:
                    sessions.backfill(_history_commands_since(active.start_marker))
                s = sessions.end()
                print(
                    f'ended session {s.id}: "{s.name}" - '
                    f"{len(s.commands)} commands in {_fmt_duration(s.duration_seconds())}"
                )
                if not s.commands and _history_path() is None:
                    print(
                        "(no commands captured - run 'snipvault init' to enable "
                        "recording on this shell)"
                    )
                print(f"View it with:  snipvault session {s.id}")
            elif args.command == "sessions":
                if args.action == "rm":
                    if args.id is None:
                        print(
                            "error: usage: snipvault sessions rm <id>",
                            file=sys.stderr,
                        )
                        return 1
                    s = sessions.remove(args.id)
                    print(f'removed session {s.id}: "{s.name}"')
                else:
                    _print_sessions(sessions.all())
            elif args.command == "session":
                if args.id == "rm":
                    if args.extra is None:
                        print("error: usage: snipvault session rm <id>", file=sys.stderr)
                        return 1
                    s = sessions.remove(int(args.extra))
                    print(f'removed session {s.id}: "{s.name}"')
                else:
                    _print_session(sessions.get(int(args.id)))
        except (ValueError, KeyError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        return 0

    vault = Vault(args.vault)

    try:
        if args.command == "add":
            tags = parse_tags(args.tags)
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
