# Changelog

All notable changes to Snippet Vault are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## v0.2.2

**Terminal sessions that just work — zero setup.** Record everything you do in the
terminal without touching a config file. Run `snipvault start`, do your work, then
`snipvault end` — on Windows PowerShell your commands are captured automatically
from your shell history. If you tried sessions before and nothing recorded, this
is the release that makes it effortless.

- Zero-setup command capture on PowerShell (no `snipvault init` needed).
- Delete a session with `snipvault session rm <id>` as well as `sessions rm <id>`.

## v0.2.1

**Keep your session list tidy.** Delete any recorded session by id, exactly like
removing a snippet — and if you delete the one that's currently recording, it stops
cleanly. A small touch that completes the sessions workflow.

- Added `snipvault sessions rm <id>`.

## v0.2.0

**The big one: record what you actually did.** Snippet Vault can now capture a whole
terminal session. `snipvault start "task"` → work → `snipvault end`, then replay a
clean log of every command you ran. Perfect for write-ups, onboarding notes, or
remembering exactly how you fixed that thing last week — and it's 100% local and
offline, like everything else.

- New `start`, `end`, `sessions`, `session`, and `init` commands.
- Sessions stored locally in `~/.snipvault-sessions.json`.

## v0.1.6

**Nothing hidden about your data.** Uninstall now shows the exact location of your
snippets and the precise command to delete them, so you're always in control. Help
displays every accepted tag format at a glance.

## v0.1.5

**Tags that don't fight you.** Type them however feels natural — `--tags web api`,
`--tags web,api`, or `--tags "web, api"` — they all just work. No more cryptic
errors from a stray space after a comma.

## v0.1.4

**A help screen that reads clean.** The command list now lines up perfectly no
matter how long the command names get. Small polish, noticeably nicer to scan.

## v0.1.3

**Uninstall in one command.** Type `snipvault uninstall` and get the exact,
OS-correct removal steps — no digging through docs.

## v0.1.2

**Never guess the syntax again.** `snipvault help` now prints a copy-paste example
for every command, right next to what it does.

## v0.1.1

**Friendly from the first keystroke.** `snipvault help` and a bare `snipvault` now
show the full command list instead of an error.

## v0.1.0

**Your code snippets, one command away.** The first release: a tiny, dependency-free,
fully offline snippet manager for your terminal. Save a command once, search it
forever. Ships as a single-file binary for Windows, macOS, and Linux — no Python, no
setup, no account. Stop re-Googling the commands you already figured out.

- Core commands: `add`, `list`, `show`, `search`, `rm`.
- One-line install/uninstall scripts and prebuilt binaries for all three platforms.
