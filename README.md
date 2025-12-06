# Command Line Conflict

"Command Line Conflict" is a fast-paced, open-source real-time strategy (RTS) game inspired by StarCraft, rendered entirely in charming ASCII art. The game features base building, unit production, resource gathering (planned), and combat between factions.

## Purpose

The project aims to demonstrate how complex game mechanics like ECS (Entity Component System), pathfinding, and fog of war can be implemented in a text-based rendering environment using Python and Pygame. It serves as an educational resource and a fun project for retro-style game enthusiasts.

## Getting Started

This guide will walk you through setting up and running the game on your local machine, as well as development best practices.

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)
- `venv` (standard library for virtual environments)

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

## Gameplay & Controls

### Main Menu
- Use **Up/Down Arrow Keys** to navigate.
- Press **Enter** to select an option.

### In-Game Controls
- **Camera Movement**: Arrow Keys or Middle Mouse Drag.
- **Zoom**: Mouse Scroll Wheel.
- **Select Units**: Left Click (click or drag box). Hold **Shift** to add to selection.
- **Move/Attack**: Right Click.
- **Build Structures**: Select a "Chassis" (worker) unit and press:
    - **R**: Rover Factory (Produces Rovers)
    - **A**: Arachnotron Factory (Produces Arachnotrons)
- **Train Units**: Select a factory (click on it).
- **Debug Commands**:
    - **1-6**: Spawn test units at cursor.
    - **F1**: Toggle Map Reveal (Fog of War).
    - **F2**: Toggle God Mode.
    - **TAB**: Switch Player Control (P1 vs P2).
    - **P**: Pause Game.
    - **H**: Hold Position.

## Development

### Project Structure
- `command_line_conflict/`: Main package directory.
    - `components/`: ECS components (data containers).
    - `systems/`: ECS systems (logic).
    - `scenes/`: Game scenes (Menu, Game, Settings).
    - `maps/`: Map definitions and pathfinding logic.
    - `utils/`: Utility functions (e.g., targeting).
- `tests/`: Unit and integration tests.

### Running Tests and Linters

Before submitting changes, ensure your code passes all checks:

```bash
# Format code
black .
isort .

# Run static analysis
black --check .
isort --check-only .

# Run tests
pytest
```

## Contributing

Please refer to `AGENTS.md` for a list of planned features and tasks. Ensure all new code includes docstrings and follows the existing style.
