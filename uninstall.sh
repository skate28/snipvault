#!/bin/sh
# Snippet Vault uninstaller for macOS and Linux. Reverses install.sh.
# Usage:  curl -fsSL https://raw.githubusercontent.com/skate28/snipvault/main/uninstall.sh | sh

set -e

INSTALL_DIR="${SNIPVAULT_INSTALL_DIR:-$HOME/.local/bin}"
BIN="$INSTALL_DIR/snipvault"
VAULT="$HOME/.snipvault.json"

echo "Uninstalling Snippet Vault..."

if [ -f "$BIN" ]; then
    rm -f "$BIN"
    echo "  removed $BIN"
else
    echo "  nothing installed at $BIN"
fi

echo ""
echo "Snippet Vault uninstalled."

# Leave the user's data in place; just tell them where it is.
if [ -f "$VAULT" ]; then
    echo "Your saved snippets are untouched at:"
    echo "  $VAULT"
    echo "Delete that file too if you want to remove your snippets:  rm $VAULT"
fi
