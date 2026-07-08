# Changelog

All notable changes to Snippet Vault are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## v0.1.5

- `--tags` now accepts spaces as well as commas, so `--tags web api`,
  `--tags web,api`, and `--tags "web, api"` all work. Previously a space after
  a comma caused an "unrecognized arguments" error.

## v0.1.4

- Fixed alignment of the `snipvault help` command list so descriptions line up
  regardless of command-name length.

## v0.1.3

- Added a `snipvault uninstall` command that prints the exact OS-specific
  removal command (a running binary can't reliably delete itself).

## v0.1.2

- `snipvault help` (and bare `snipvault`) now print a friendly command list with a
  copy-paste example for each command, plus notes on optional flags.
- Help text is ASCII-only to avoid Windows console encoding issues.

## v0.1.1

- Added a `help` command; bare `snipvault` now shows help instead of an error.

## v0.1.0

- First release: `add`, `list`, `show`, `search`, and `rm` commands backed by a
  local JSON vault (`~/.snipvault.json`).
- Prebuilt single-file binaries for Windows, macOS, and Linux.
- One-line install/uninstall scripts and a `pip install` from source option.
- Landing page with OS-detected downloads.
