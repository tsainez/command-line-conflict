# Command Line Conflict

"Command Line Conflict" is a codename for a fast-paced, open-source real-time strategy game inspired by Starcraft, rendered entirely in charming ASCII art.

## Getting Started

This guide will walk you through setting up and running the game on your local machine, as well as development best practices. 

### Prerequisites

- Python 3.8 or higher
- `pip` and `venv`

### Cross-Platform Environment Setup

To run the game manually, your system must know where to find Python. If running `python --version` or `pip --version` fails, follow these steps to add Python to your system's PATH.

#### Windows 11
1.  **Search for "Environment Variables"**: Open the Start menu, type "env", and select **"Edit the system environment variables"**.
2.  **Environment Variables**: Click the **"Environment Variables..."** button.
3.  **Edit Path**: In the "User variables" section, locate the row named **"Path"** and double-click it.
4.  **Add Python Paths**: Click **"New"** and add the paths to your Python executable and Scripts folder. They usually look like this (replace `YourUsername` and version number):
    *   `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\`
    *   `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts\`
5.  **Apply**: Click OK on all dialogs and restart your terminal (PowerShell or Command Prompt).

#### macOS
If you installed Python via the official installer, it likely set the PATH for you. If not, or if using Homebrew:
1.  Open your terminal.
2.  Edit your shell profile (e.g., `~/.zshrc` or `~/.bash_profile`):
    ```bash
    nano ~/.zshrc
    ```
3.  Add the following line (adjusting for your specific installation path):
    ```bash
    export PATH="/usr/local/bin:$PATH"
    # or for Homebrew on Apple Silicon:
    export PATH="/opt/homebrew/bin:$PATH"
    ```
4.  Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`), then reload:
    ```bash
    source ~/.zshrc
    ```

#### Linux
Most Linux distributions come with Python installed. If you installed a custom version:
1.  Open your terminal.
2.  Edit your `.bashrc` or `.zshrc`:
    ```bash
    nano ~/.bashrc
    ```
3.  Add the export line pointing to your Python bin directory:
    ```bash
    export PATH="/path/to/python/bin:$PATH"
    ```
4.  Reload the configuration:
    ```bash
    source ~/.bashrc
    ```

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