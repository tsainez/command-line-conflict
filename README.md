# Command Line Conflict

"Command Line Conflict" is a fast-paced, open-source real-time strategy game inspired by classic RTS games, rendered entirely in a charming ASCII art style. Players build units, manage resources, and command their armies to defeat the opponent.

## Features

- **Classic RTS Gameplay**: Experience the core mechanics of real-time strategy, including base building, resource gathering (implied), and tactical combat.
- **ASCII Art Style**: A unique, minimalist aesthetic that runs smoothly on any terminal that supports pygame.
- **Variety of Units**: Command a diverse roster of units, from the basic Chassis to the powerful Immortal, each with unique stats and abilities.
- **Fog of War**: Explore the map and uncover enemy positions with strategic scouting.
- **Extensible Engine**: Built with a clean Entity-Component-System (ECS) architecture that is easy to understand and extend.

## Getting Started

This guide will walk you through setting up and running the game on your local machine.

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
    The game will start in the main menu.

## How to Play

### Controls

- **Camera Movement**: Use the **Arrow Keys** or **W, A, S, D** to move the camera.
- **Camera Zoom**: Use the **Mouse Wheel** to zoom in and out.
- **Select Units**:
    - **Click** on a unit to select it.
    - **Hold Shift and Click** to add or remove units from your selection.
    - **Click and Drag** to select all units within a rectangular area.
- **Move Units**: Select one or more units and **Right-Click** on a destination.
- **Create Units**: Press the corresponding number key to create a unit at the mouse cursor's location.
- **Pause Game**: Press **P** to pause or unpause the game.
- **Return to Menu**: Press **Escape** to return to the main menu from the game.

### Unit Creation Hotkeys

- **1**: Extractor
- **2**: Chassis
- **3**: Rover
- **4**: Arachnotron
- **5**: Observer
- **6**: Immortal
- **W**: Wall (Note: This is a stationary defensive structure)

## Project Structure

The project is organized using an Entity-Component-System (ECS) architecture.

- **`main.py`**: The main entry point of the application.
- **`command_line_conflict/`**: The core game module.
  - **`engine.py`**: Contains the main `Game` class and the `SceneManager`.
  - **`game_state.py`**: Manages the state of all entities and components.
  - **`components/`**: Defines the data for entities (e.g., `Position`, `Health`, `Attack`).
  - **`systems/`**: Implements the logic that operates on components (e.g., `MovementSystem`, `CombatSystem`).
  - **`scenes/`**: Manages the different game screens (e.g., `MenuScene`, `GameScene`).
  - **`maps/`**: Defines the game maps.
  - **`factories.py`**: Contains functions for creating pre-defined units.
  - **`config.py`**: Contains global configuration variables.
  - **`logger.py`**: Sets up the application logger.

## Development

Before a change can be safely integrated, it must pass linting and automated tests.

Run the checks:

```bash
# Check code formatting with Black
black --check .

# Check import sorting with isort
isort --check-only .

# Run the test suite with pytest
pytest -q
```