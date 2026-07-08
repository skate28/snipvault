"""Command-line interface for Snippet Vault."""

from __future__ import annotations

import argparse
import sys

from .storage import DEFAULT_VAULT, Snippet, Vault

# (command, one-line description, example of exactly what to type)
COMMANDS = [
    ("add", "Save a snippet", 'snipvault add "title" "code here" --lang python --tags tag1,tag2'),
    ("list", "List all your snippets", "snipvault list"),
    ("search", "Search titles, languages, tags, and code", "snipvault search keyword"),
    ("show", "Print a snippet's code by its id", "snipvault show 1"),
    ("rm", "Delete a snippet by its id", "snipvault rm 1"),
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
    print("This removes the snipvault binary and its PATH entry. Your saved")
    print("snippets in ~/.snipvault.json are kept - delete that file yourself")
    print("if you also want to erase your data.")
    print("(If you installed with pip instead: pip uninstall snipvault)")


def print_help() -> None:
    """Print a friendly command list with a copy-paste example for each."""
    print("snipvault - store and retrieve code snippets locally\n")
    print("Usage: snipvault <command> [options]\n")
    print("Commands:")
    for name, desc, example in COMMANDS:
        print(f"  {name:<7} {desc}")
        print(f"          $ {example}")
    print()
    print("Notes:")
    print("  --lang and --tags are optional; tags are comma-separated (tag1,tag2).")
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="snipvault", description="Store and retrieve code snippets locally."
    )
    parser.add_argument(
        "--vault", default=str(DEFAULT_VAULT), help="path to the vault JSON file"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("help", help="show this help message")

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
