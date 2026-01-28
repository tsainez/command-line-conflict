# Scripts

This directory contains utility scripts for development and maintenance of the Command Line Conflict project.

## `pre_commit.sh`

This script runs a suite of checks to ensure code quality before you commit your changes. It is the same set of checks that are run in the Continuous Integration (CI) pipeline.

### Usage

Run from the root of the repository:

```bash
./scripts/pre_commit.sh
```

### What it checks:

1.  **Black**: Checks code formatting.
2.  **Isort**: Checks import sorting.
3.  **Flake8**: Checks for style and syntax errors.
4.  **Pylint**: Checks for code quality and bugs (enforces a score >= 9.0).
5.  **Pytest**: Runs unit tests and checks code coverage (must be >= 80%).

## Note

Ensure you have your virtual environment activated and dependencies installed (`pip install -r requirements.txt`) before running these scripts.
