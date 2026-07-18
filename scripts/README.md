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

## `pr_merge_optimizer/`

A standalone tool that analyzes a batch of open pull requests, builds a pairwise
conflict graph, and computes the largest **conflict-free batch** of pull requests
that can be merged at once (a Maximum Independent Set problem). Pull requests left
over are flagged for manual or agentic conflict resolution.

### Usage

Run as a module from the repository root:

```bash
# From a JSON description of the pull requests
python -m scripts.pr_merge_optimizer --input plan.json

# Live from GitHub (uses GITHUB_TOKEN if set)
python -m scripts.pr_merge_optimizer --repo tsainez/command-line-conflict
```

See [`docs/PRMergeOptimizer.md`](../docs/PRMergeOptimizer.md) for the input
format, all flags, and the game/RTS asset handling.

## Note

Ensure you have your virtual environment activated and dependencies installed (`pip install -r requirements.txt`) before running these scripts.
