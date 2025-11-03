#!/usr/bin/env bash
set -euo pipefail

echo "Running comprehensive Talk to Unity regression tests..."
python -m unittest discover -s tests -p 'test_*.py' -v
