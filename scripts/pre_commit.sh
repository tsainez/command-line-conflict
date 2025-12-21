#!/bin/bash
set -e

echo "Running Black..."
black .

echo "Running isort..."
isort .

echo "Running Flake8..."
flake8 .

echo "Running Pylint..."
# Check if we are in a git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
    pylint $(git ls-files '*.py')
else
    echo "Not a git repository, scanning all .py files..."
    pylint $(find . -name "*.py" -not -path "./.venv/*")
fi

echo "Running Tests..."
export SDL_VIDEODRIVER=dummy
pytest --cov=command_line_conflict tests/

echo "All checks passed!"
