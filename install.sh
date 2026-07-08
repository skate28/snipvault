#!/bin/sh
# Snippet Vault installer for macOS and Linux.
# Usage:  curl -fsSL https://raw.githubusercontent.com/skate28/snipvault/main/install.sh | sh

set -e

REPO="skate28/snipvault"
INSTALL_DIR="${SNIPVAULT_INSTALL_DIR:-$HOME/.local/bin}"

case "$(uname -s)" in
    Darwin) ASSET="snipvault-macos-arm64" ;;
    Linux)  ASSET="snipvault-linux-x64" ;;
    *) echo "error: unsupported OS: $(uname -s)" >&2; exit 1 ;;
esac

URL="https://github.com/$REPO/releases/latest/download/$ASSET"

echo "Installing Snippet Vault..."
mkdir -p "$INSTALL_DIR"

echo "  downloading $URL"
if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$URL" -o "$INSTALL_DIR/snipvault"
else
    wget -qO "$INSTALL_DIR/snipvault" "$URL"
fi
chmod +x "$INSTALL_DIR/snipvault"

# Verify it runs.
"$INSTALL_DIR/snipvault" --help >/dev/null

echo ""
echo "Snippet Vault installed to $INSTALL_DIR/snipvault"
case ":$PATH:" in
    *":$INSTALL_DIR:"*) echo "Try:  snipvault --help" ;;
    *)
        echo "NOTE: $INSTALL_DIR is not on your PATH. Add this to your shell profile:"
        echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
        ;;
esac
