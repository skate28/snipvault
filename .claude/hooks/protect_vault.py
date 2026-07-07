"""PreToolUse hook: block any tool call that targets the user's real vault file.

Claude Code pipes the pending tool call as JSON on stdin. Exit code 2 blocks
the call and feeds stderr back to Claude as the reason.
"""

import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed input - don't block

    tool_input = json.dumps(payload.get("tool_input", {})).replace("\\\\", "/")
    if ".snipvault.json" in tool_input:
        print(
            "Blocked: this call references ~/.snipvault.json, the user's real "
            "snippet vault. Never read, edit, or delete it directly. Use the "
            "snipvault CLI for vault operations, and temp vault files "
            "(--vault <temp path>) for tests and demos.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
