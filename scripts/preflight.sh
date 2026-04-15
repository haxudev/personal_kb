#!/usr/bin/env bash
set -euo pipefail

errors=0

if ! command -v markitdown &>/dev/null; then
  echo "ERROR: markitdown not found. Install: pip install 'markitdown[all]'" >&2
  errors=$((errors + 1))
fi

if ! command -v rg &>/dev/null; then
  echo "WARN: ripgrep (rg) not found. Install: brew install ripgrep / apt install ripgrep" >&2
  echo "      Falling back to grep will work but is slower." >&2
fi

if [ $errors -gt 0 ]; then
  echo "Preflight check failed with $errors error(s)." >&2
  exit 1
fi

echo "Preflight check passed."
