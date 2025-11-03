#!/usr/bin/env bash
set -euo pipefail

if ! grep -q "<title>" index.html; then
  echo "index.html is missing a <title> element"
  exit 1
fi

echo "Verified that index.html contains a <title> element."
