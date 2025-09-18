# Command Line Conflict

"Command Line Conflict" is a codename for a fast-paced, open-source real-time strategy game inspired by Starcraft, rendered entirely in charming ASCII art.

## Getting Started

This guide will walk you through setting up and running the game on your local machine, as well as development best practices. 

### Prerequisites

- Python 3.8 or higher
- `pip` and `venv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/command-line-conflict.git
    cd command-line-conflict
    ```

2.  **Create and activate a virtual environment:**
    This isolates the project's dependencies from your system's Python installation.
    ```bash
    # For macOS and Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Launch the game:**
    ```bash
    python main.py
    ```

### (Optional) Running Tests and Linters
Before a change can be safely integrated, it must first pass through linting, automated testing, and finally a human player's assessment. 

Run the checks:

    ```bash
    # Check code formatting with Black
    black --check .

    # Check import sorting with isort
    isort --check-only .

    # Run the test suite with pytest
    pytest -q
    ```