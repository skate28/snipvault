"""PyInstaller entry point.

A plain top-level script (rather than snipvault/__main__.py, which uses
relative imports) so PyInstaller can bundle the package reliably.
"""

from snipvault.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
