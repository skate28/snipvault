# Snippet Vault — Roadmap & History

This is the living roadmap. Work is organized into three product versions.
Check items off (`[x]`) as they are completed.

Semantic-version mapping: **Version 1** = the local tool (`0.x` → `1.0.0`),
**Version 2** = cloud SaaS (`2.x`), **Version 3** = AI (`3.x`).

---

## Version 1 — Local tool (semver 0.x → 1.0.0)

The private, offline, dependency-free terminal tool.

### Shipped (v0.1.0 – v0.1.6)
- [x] Core CLI: `add`, `list`, `show`, `search`, `rm`
- [x] Local JSON vault storage (`~/.snipvault.json`)
- [x] `help` command + bare-invocation help with per-command examples
- [x] `uninstall` command (shows data-file path + delete command)
- [x] Flexible `--tags` (spaces or commas)
- [x] Cross-platform single-file binaries (Windows/macOS/Linux)
- [x] Tag-triggered release CI + test CI (GitHub Actions)
- [x] One-line install/uninstall scripts
- [x] Landing page deployed to Vercel
- [x] LICENSE, CHANGELOG, README command reference, full docs
- [x] Agent tooling: AGENTS.md, skills, test-guardian subagent, pre-commit gate

### In progress — v0.2.0: Terminal Sessions
- [x] `history.md` roadmap created
- [x] Session data model + JSON store (`snipvault/sessions.py`)
- [x] `snipvault start [name]` / `snipvault end`
- [x] Shell-hook command capture (`snipvault init` + hidden `_record`)
- [x] `snipvault sessions` (list) + `snipvault session <id>` (formatted, timestamped log)
- [x] Tests (SessionStore + CLI)
- [ ] Docs updated (README, CHANGELOG, help, docs, website version)
- [ ] Released as tag `v0.2.0`

### Later in Version 1
- [ ] Declare the local tool stable → cut `v1.0.0`

---

## Version 2 — Cloud SaaS (semver 2.x)

Opt-in cloud mode; local mode stays fully private forever.

- [ ] Local vs cloud mode choice
- [ ] Authentication + accounts
- [ ] Supabase database + sync of snippets and sessions
- [ ] Web dashboard: snippets, sessions, timestamps, graphical terminal history
- [ ] Automatic secret redaction before anything is uploaded (privacy)

---

## Version 3 — AI (semver 3.x)

Local, offline AI assistance.

- [ ] Local Ollama integration (pluggable backend, opt-in)
- [ ] Smart auto-tagging on `add`
- [ ] Natural-language search over snippets/sessions
- [ ] Graceful fallback when no AI backend is configured
