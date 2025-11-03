#!/usr/bin/env bash
set -euo pipefail

echo "Running Talk to Unity smoke tests for pull requests..."
python -m unittest discover -s test -p 'test_*.py' -v
