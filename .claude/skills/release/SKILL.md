---
name: release
description: Cut a new Snippet Vault release - bump the version in both places, run the full test suite, reinstall, and smoke-test the CLI. Use when the user asks to release, bump the version, or ship a new version.
---

# Release Snippet Vault

Follow these steps in order. Stop and report if any step fails.

1. **Determine the new version.** Ask the user for the bump type if not given
   (patch / minor / major). Read the current version from `pyproject.toml`.

2. **Bump the version in BOTH places** (they must stay in sync):
   - `pyproject.toml` → `version = "X.Y.Z"`
   - `snipvault/__init__.py` → `__version__ = "X.Y.Z"`

3. **Run the full test suite:**
   ```
   python -m unittest discover -s tests -v
   ```
   If anything fails, revert the version bump and report the failure. Do not proceed.

4. **Reinstall the package:**
   ```
   python -m pip install -e .
   ```

5. **Smoke-test the installed CLI:**
   ```
   snipvault --help
   ```
   Confirm it prints usage without errors.

6. **If the project is a git repository**, stage the two version files and show
   the user the diff. Only commit if the user asks, using the message
   `release: vX.Y.Z`.

7. **Report:** old version → new version, test counts, and smoke-test result.
