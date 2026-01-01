# Development Guide

This guide provides detailed instructions for setting up the development environment, running tests, debugging, and building the project.

## Environment Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/tsainez/command-line-conflict.git
    cd command-line-conflict
    ```

2.  **Create a Virtual Environment**:
    We recommend using a virtual environment to manage dependencies.
    ```bash
    python -m venv .venv
    # Activate on Linux/macOS:
    source .venv/bin/activate
    # Activate on Windows:
    .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

To start the game from the source:
```bash
python main.py
```

## Running Tests

We use `pytest` for testing. The configuration is stored in `pytest.ini`.

### Run All Tests
```bash
python -m pytest
```

### Run Specific Tests
You can run tests for a specific file or directory:
```bash
python -m pytest tests/unit/systems/test_movement_system.py
```

### Run with Coverage
To generate a coverage report:
```bash
python -m pytest --cov=command_line_conflict --cov-report=html
```
Open `htmlcov/index.html` in your browser to view the report.

### Headless Testing
The CI environment runs tests in "headless" mode (without a display). You can simulate this locally:
```bash
export SDL_VIDEODRIVER="dummy"
python -m pytest
```

## Debugging

### Debug Mode
The `config.py` file contains a `DEBUG` flag.
*   **Default**: `False`
*   **Enable**: Set `DEBUG = True` in `command_line_conflict/config.py` (do not commit this change).

When `DEBUG` is enabled:
*   Cheat keys are active (e.g., `F1` for Reveal Map).
*   Additional logging is output to the console.
*   Performance metrics may be displayed.

### Logs
The game logs to both the console and a file.
*   **Log File**: Located in the user data directory (platform dependent).
*   **Console**: Standard output.

## Code Quality

We use several tools to ensure code quality.

### Pre-Commit Script
Run the pre-commit script before submitting a PR to check for common issues:
```bash
./scripts/pre_commit.sh
```

### Manual Checks
*   **Format**: `black .` and `isort .`
*   **Lint**: `flake8 .` and `pylint command_line_conflict/`
*   **Type Check**: `mypy command_line_conflict/`

## Building the Executable

We use `PyInstaller` to build a standalone executable.

```bash
python build.py
```
The output will be in the `dist/` directory.
