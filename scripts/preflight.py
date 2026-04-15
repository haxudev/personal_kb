#!/usr/bin/env python3
"""Cross-platform preflight checks for personal_kb."""

from __future__ import annotations

import platform
import shutil
import sys


def detect_shell() -> str:
    if platform.system() == "Windows":
        if "pwsh" in (shutil.which("pwsh") or ""):
            return "windows-powershell-compatible"
        return "windows-cmd-compatible"
    return "posix-shell"


def main() -> int:
    errors = 0
    shell = detect_shell()
    print(f"Detected environment: {platform.system()} / {shell}")

    if shutil.which("markitdown") is None:
        print('ERROR: markitdown not found. Install with: pip install "markitdown[all]"', file=sys.stderr)
        errors += 1

    if shutil.which("rg") is None:
        print("WARN: ripgrep (rg) not found.", file=sys.stderr)
        if platform.system() == "Windows":
            print("      Install via winget: winget install BurntSushi.ripgrep.MSVC", file=sys.stderr)
        else:
            print("      Install via brew install ripgrep / apt install ripgrep", file=sys.stderr)
        print("      Falling back to grep/findstr may work but is slower.", file=sys.stderr)

    if errors:
        print(f"Preflight check failed with {errors} error(s).", file=sys.stderr)
        return 1

    print("Preflight check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
