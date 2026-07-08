# Changelog

All notable changes to Snippet Vault are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## v0.2.2

- **Sessions now work on PowerShell with no setup.** At `end`, commands are read
  from the PowerShell history file, so `snipvault init` is no longer required on
  Windows (it stays optional, adding per-command timestamps via a live hook).
- `snipvault session rm <id>` now works too, alongside `snipvault sessions rm <id>`.

## v0.2.1

- Added `snipvault sessions rm <id>` to delete a recorded session by its id
  (mirrors `snipvault rm` for snippets). Deleting the active session stops recording.

## v0.2.0

Adds **terminal sessions** — record the commands you run during a work session
and review them later. Fully local; no database.

- `snipvault start [name]` / `snipvault end` to record a session.
- `snipvault init` sets up a shell hook (PowerShell/bash/zsh) that logs commands
  while a session is active — zero overhead otherwise, and it never records your
  snipvault commands.
- `snipvault sessions` lists recorded sessions; `snipvault session <id>` prints a
  timestamped command log.
- Sessions stored locally in `~/.snipvault-sessions.json`.

## v0.1.6

- `snipvault uninstall` now shows the full path to your snippet file and the
  exact command to delete it, and makes clear your data is kept by default.
- `snipvault help` now shows the accepted tag formats (spaces, commas, or both).

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
