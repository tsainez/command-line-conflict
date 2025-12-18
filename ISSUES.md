# Issues Identified from TODOs

## 1. Implement Factory Map for Gameplay
**Location:** `command_line_conflict/factories.py`
**Original TODO:** `# TODO: Create a map with factories for the player to fight against.`

**Description:**
The game currently lacks a map specifically designed for player vs factory combat, which is hinted at in the factories module. We need to implement a `FactoryMap` class.

**Instructions:**
1.  Create a new file `command_line_conflict/maps/factory_map.py`.
2.  Implement a `FactoryMap` class inheriting from `Map` (from `command_line_conflict.maps.base`).
3.  Define the map dimensions (e.g., 40x30).
4.  Override the initialization or create a setup method to:
    *   Add walls/obstacles to define the arena.
    *   Spawning logic is currently handled in `GameScene`, but `FactoryMap` should ideally provide a layout or hook for this. For now, implement the map structure.
5.  (Optional) Refactor `GameScene` to use `FactoryMap` or allow map selection.
6.  Once implemented, remove the TODO comment from `command_line_conflict/factories.py`.

## 2. Complete Project Structure Documentation
**Location:** `docs/ProjectStructure.md`
**Original TODO:** `TODO:: ADD SOMETHING HERE!`

**Description:**
The project structure documentation is currently empty.

**Instructions:**
1.  Edit `docs/ProjectStructure.md`.
2.  Add a description of the repository layout:
    *   `command_line_conflict/`: Source code package.
    *   `tests/`: Unit and integration tests.
    *   `docs/`: Documentation.
    *   `scripts/`: Utility scripts.
3.  Describe key modules:
    *   `main.py`: Application entry point.
    *   `engine.py`: Game loop and scene management.
    *   `game_state.py`: ECS data holder.
    *   `systems/`: Game logic systems.
    *   `components/`: Entity data components.
4.  Remove the TODO placeholder.
