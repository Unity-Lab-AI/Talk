#!/usr/bin/env bash
set -euo pipefail

echo "Checking that index.html exists..."
[ -f "index.html" ]
echo "Checking that landing.js exists..."
[ -f "landing.js" ]
echo "Checking that style.css exists..."
[ -f "style.css" ]

echo "All required site files are present."
