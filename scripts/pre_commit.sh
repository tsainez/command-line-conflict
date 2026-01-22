#!/bin/bash
set -e

echo "🧹 Choremaster: Starting pre-commit checks..."

# Check if we are in the root directory by looking for pyproject.toml
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root."
    exit 1
fi

echo "🎨 Running Black..."
black --check .

echo "📚 Running isort..."
isort --check-only .

echo "🔍 Running Flake8..."
flake8 .

echo "🧐 Running Pylint..."
# Use git ls-files to get tracked files, or fallback to find
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    FILES=$(git ls-files '*.py')
else
    FILES=$(find . -name "*.py" -not -path "*/.*" -not -path "*/venv/*")
fi

# Run pylint on the file list. usage of xargs is safer for long lists but keeping it simple for now as per CI
# We enforce a score of 9.0 to maintain code quality while allowing some non-critical warnings
pylint $FILES --fail-under=9.0

echo "🧪 Running Tests..."
export SDL_VIDEODRIVER=dummy
python -m pytest

echo "✅ All checks passed! Ready to commit."
