# Contributing to Command Line Conflict

Thank you for your interest in contributing to Command Line Conflict! We welcome contributions from everyone.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/command-line-conflict.git
    cd command-line-conflict
    ```
3.  **Set up your environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```

## Project Structure

Before diving in, it's helpful to understand the codebase organization. Please read:
*   [Project Structure](docs/ProjectStructure.md) - Overview of files and modules.
*   [ECS Architecture](docs/ECS.md) - Guide to the Entity-Component-System design pattern used in the game.

## Finding Tasks

We have a backlog of potential tasks suitable for both human contributors and autonomous agents:

*   **[AGENTS.md](AGENTS.md)**: A list of 100 features, improvements, and refactoring tasks. This is the best place to find something to work on.
*   **[ISSUES.md](ISSUES.md)**: A collection of known technical debt and code cleanup items.
*   **GitHub Issues**: Check the open issues on the repository.

## Development Workflow

1.  **Create a branch** for your feature or bugfix:
    ```bash
    git checkout -b feature/my-new-feature
    ```
2.  **Make your changes**.
3.  **Run tests and linters** locally to ensure everything is correct (see below).
4.  **Commit your changes** with a descriptive commit message.
5.  **Push to your fork** and submit a Pull Request.

## Code Style & Linting

We enforce a strict code style to keep the codebase clean and maintainable.

*   **Line Length:** Maximum 127 characters.
*   **Formatter:** We use `black`.
*   **Import Sorting:** We use `isort`.
*   **Linting:** We use `flake8` and `pylint`.

### Running Checks
We have provided a convenience script to run all checks. **You must run this command before submitting your PR:**

```bash
./scripts/pre_commit.sh
```

This script will run:
*   **Formatting:** `black` and `isort`
*   **Linting:** `flake8` and `pylint`
*   **Testing:** `pytest` with coverage

Ensure the script exits with "All checks passed!" before pushing your changes.

### Logging
*   Avoid wrapping `log.debug()` calls with `if config.DEBUG:`. Rely on the logging library's level filtering instead.

## Pull Requests

Please use the provided Pull Request Template (`.github/pull_request_template.md`) when opening a PR.

*   **Title:** Use a descriptive title (e.g., "Add delta-time to unit movement", "Fix crash in map loader").
*   **Scope:** Keep PRs small and focused on a single feature or bug fix.
*   **Description:** Include details about what was changed and why.
*   **Smoke Tests:** Include basic smoke tests or verification steps in your PR description, especially when changing core logic.
*   **CI:** All CI checks must pass before merging.

## Reporting Bugs / Security

*   **Bugs:** Open an issue on GitHub with steps to reproduce.
*   **Security:** Please refer to the [Security Policy](SECURITY.md) for reporting vulnerabilities.

## Feature Requests

We welcome feature ideas! Open an issue to discuss your proposal before starting work to ensure it aligns with the project goals.
