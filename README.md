# Command Line Conflict

A fast-paced, open-source RTS game inspired by Starcraft, rendered entirely in charming ASCII art and designed for cross-platform play.

## Getting Started

This guide will walk you through setting up and running the game on your local machine.

> **Note for Windows users:** For detailed, step-by-step instructions, please see our [Windows Installation Guide](docs/WindowsInstallation.md).

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

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
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

To ensure code quality and catch errors early, you can run the linters and tests.

1.  **Install development dependencies:**
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Run the checks:**
    ```bash
    # Check code formatting with Black
    black --check .

    # Check import sorting with isort
    isort --check-only .

    # Run the test suite with pytest
    pytest -q
    ```

### (Optional) Bundling into an Executable

You can bundle the game into a single standalone executable using PyInstaller.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the bundler:**
    ```bash
    pyinstaller --onefile main.py
    ```
    The executable will be created in the `dist/` directory.

## Usage

### Main Menu

When you launch the game, you will be greeted by the main menu. Use the **Up** and **Down** arrow keys to navigate the options and **Enter** to select one.

-   **New Game:** Starts a new game.
-   **Options:** Opens the settings menu.
-   **Quit:** Exits the game.

### Controls

#### Mouse

-   **Left-click and drag:** Select one or more units.
-   **Shift + Left-click:** Add or remove a unit from the current selection.
-   **Right-click:** Issue a move command to all selected units. If an enemy is right-clicked, the selected units will attack it.

#### Keyboard

The following keys can be used to spawn units and structures at the current mouse cursor position:

-   **1:** Spawn an **Extractor**
-   **2:** Spawn a **Chassis**
-   **3:** Spawn a **Rover**
-   **4:** Spawn an **Arachnotron**
-   **5:** Spawn an **Observer**
-   **6:** Spawn an **Immortal**
-   **W:** Place a **Wall**

Other keyboard shortcuts:

-   **Q:** Quit the game immediately.
-   **ESC:** Return to the main menu from the game or settings screen.

### Unit Types

For detailed information about each unit's stats and special abilities, please see the [Unit Types Documentation](docs/UnitTypes.md).

## Documentation

For more detailed documentation, please see the following files in the `docs` directory:

*   [Windows Installation](docs/WindowsInstallation.md)
*   [Project Structure](docs/ProjectStructure.md)
*   [Maps](docs/Maps.md)
*   [Unit Types](docs/UnitTypes.md)
*   [Controls](docs/Controls.md)
*   [Contributing](docs/Contributing.md)
