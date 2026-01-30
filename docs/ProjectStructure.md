# Project Structure

This document outlines the file organization and key modules of the **Command Line Conflict** repository.

## Directory Layout

The project follows a standard Python package structure.

```text
command-line-conflict/
├── .github/                 # GitHub Actions workflows and templates
│   ├── ISSUE_TEMPLATE/      # Bug report and feature request templates
│   ├── workflows/           # CI/CD pipelines (ci.yml, tests.yml, etc.)
│   └── pull_request_template.md
├── command_line_conflict/   # Main game source code
│   ├── components/          # ECS Components (Data)
│   ├── maps/                # Map definitions and loading logic
│   ├── scenes/              # Game States (Menu, Game, etc.)
│   ├── systems/             # ECS Systems (Logic)
│   ├── ui/                  # Reusable UI widgets
│   ├── utils/               # Utility helper functions
│   ├── config.py            # Global configuration
│   ├── engine.py            # Main game loop and scene management
│   ├── factories.py         # Entity creation factories
│   └── game_state.py        # Central data holder for the game
├── docs/                    # Documentation (MkDocs)
├── scripts/                 # Maintenance scripts (pre-commit, etc.)
├── tests/                   # Test suite (pytest)
│   ├── integration/         # Integration tests
│   ├── security/            # Security-focused tests
│   └── unit/                # Unit tests for individual modules
├── AGENTS.md                # Task backlog for AI agents
├── CONTRIBUTING.md          # Contribution guidelines
├── ISSUES.md                # Known issues and code cleanup tasks
├── README.md                # Project overview and instructions
├── TODO_ISSUES.md           # Instructions for specific pending tasks
├── build.py                 # PyInstaller build script
├── main.py                  # Application entry point
├── mkdocs.yml               # Documentation configuration
└── requirements.txt         # Project dependencies
```

## detailed Architecture

The game uses an **Entity-Component-System (ECS)** architecture to manage game objects and logic.

### Core Modules

*   **`main.py`**: The entry point. Initializes the engine and starts the application.
*   **`command_line_conflict/engine.py`**: Manages the main game loop, time deltas, and the `SceneManager` which transitions between different game states.
*   **`command_line_conflict/game_state.py`**: The heart of the ECS. It stores all entities and their components, manages the spatial hash map for performance, and handles the event queue.
*   **`command_line_conflict/config.py`**: Contains global constants, configuration settings, and debug flags.
*   **`command_line_conflict/logger.py`**: Configures the application-wide logging system.

### ECS Components (`command_line_conflict/components/`)

Components are pure data containers attached to entities.

*   `attack.py`: Defines damage, range, and attack speed.
*   `base.py`: Base component class.
*   `confetti.py`: Confetti particle data.
*   `dead.py`: Tag component for dead entities.
*   `detection.py`: Defines detection range.
*   `factory.py`: Data for buildings that produce units.
*   `flee.py`: State for fleeing units.
*   `health.py`: Manages HP, max HP, and regeneration.
*   `movable.py`: Stores velocity, target destination, and pathfinding state.
*   `player.py`: Identifies which player owns the entity.
*   `position.py`: Stores x, y coordinates.
*   `renderable.py`: Defines how an entity looks (character, color).
*   `selectable.py`: Marks an entity as selectable by the player.
*   `unit_identity.py`: Stores unique unit names or IDs.
*   `vision.py`: Defines the vision range for Fog of War.
*   `wander.py`: State for wandering units.

### ECS Systems (`command_line_conflict/systems/`)

Systems contain the logic that operates on entities with specific components.

*   `ai_system.py`: Controls AI behavior for non-human players.
*   `chat_system.py`: Manages in-game chat.
*   `combat_system.py`: Manages target acquisition, attacking, and damage calculation.
*   `confetti_system.py`: Manages confetti particles (visual effects).
*   `corpse_removal_system.py`: Removes dead entities after a delay.
*   `flee_system.py`: Handles logic for units fleeing from combat.
*   `health_system.py`: Manages health regeneration and death checks.
*   `movement_system.py`: Updates positions, handles pathfinding (A*), and collision avoidance.
*   `production_system.py`: Handles unit production queues in buildings.
*   `rendering_system.py`: Handles drawing entities, the map, Fog of War, and UI overlays to the screen.
*   `selection_system.py`: Manages entity selection by the player.
*   `sound_system.py`: Listens for game events and plays appropriate sound effects.
*   `spawn_system.py`: Handles spawning of new entities.
*   `ui_system.py`: Renders the Heads-Up Display (HUD), selection boxes, and tooltips.
*   `wander_system.py`: Controls idle wandering behavior for units.

### Scenes (`command_line_conflict/scenes/`)

The game is divided into distinct states or "scenes".

*   `menu.py`: The main menu.
*   `game.py`: The core gameplay loop (`GameScene`).
*   `editor.py`: The built-in map editor.
*   `settings.py`: Configuration menu.
*   `victory.py` / `defeat.py`: End-of-game screens.

### Maps (`command_line_conflict/maps/`)

*   `base.py`: Defines the `Map` base class and file loading/saving logic.
*   `simple_map.py`: A basic empty map.
*   `wall_map.py`: A map with randomly generated walls.

### UI (`command_line_conflict/ui/`)

Reusable UI components.

*   `file_dialog.py`: A modal file picker for saving/loading maps.

### Testing (`tests/`)

*   **Unit Tests**: Located in `tests/unit/`, mirroring the source structure. Focus on individual functions and classes.
*   **Integration Tests**: Located in `tests/integration/`. Test the interaction between multiple systems (e.g., game flow).
*   **Security Tests**: Located in `tests/security/`. Verify fixes for vulnerabilities (DoS, path traversal, cheat protection).
