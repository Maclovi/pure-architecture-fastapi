#!/bin/sh
set -e

echo "Running mypy..."
mypy --config-file pyproject.toml

echo "Running bandit..."
bandit -c pyproject.toml -r src

echo "Running semgrep..."
semgrep scan --config auto --error
