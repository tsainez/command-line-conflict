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

## 3. Remove Unused Imports
**Locations:**
*   `command_line_conflict/engine.py`
*   `command_line_conflict/systems/combat_system.py`
*   `command_line_conflict/systems/selection_system.py`
*   `command_line_conflict/systems/ui_system.py`

**Original TODOs:**
*   `# TODO: Remove unused import.`

**Description:**
Several files contain unused imports which clutter the code and can be confusing.

**Instructions:**
1.  Remove `import os` from `command_line_conflict/engine.py`.
2.  Remove `Player` and `Vision` imports from `command_line_conflict/systems/combat_system.py` if they are indeed unused.
3.  Remove `config` import from `command_line_conflict/systems/selection_system.py`.
4.  Remove `import math` from `command_line_conflict/systems/ui_system.py`.
5.  Remove the corresponding TODO comments.

## 4. Fix Logic Bug and Unused Variables in Game Scene
**Location:** `command_line_conflict/scenes/game.py`
**Original TODO:** `# TODO: Fix bug - should likely get UnitIdentity, or remove if unused.`

**Description:**
In `GameScene`, the variable `unit_identity` is assigned the result of `components.get(Selectable)`, which appears to be a copy-paste error (should likely be `UnitIdentity`). Furthermore, the variable is unused.

**Instructions:**
1.  Analyze `command_line_conflict/scenes/game.py`.
2.  Determine if `unit_identity` is needed.
3.  If needed, change `components.get(Selectable)` to `components.get(UnitIdentity)` (importing `UnitIdentity` if necessary).
4.  If not needed, remove the assignment entirely.
5.  Remove the TODO comment.

## 5. Remove Unused Variable in Rendering System
**Location:** `command_line_conflict/systems/rendering_system.py`
**Original TODO:** `# TODO: Remove unused variable.`

**Description:**
The `player` variable is assigned but never used in the rendering loop.

**Instructions:**
1.  Remove the line `player = components.get(Player)`.
2.  Remove the TODO comment.

## 6. Fix F-string in Editor Scene
**Location:** `command_line_conflict/scenes/editor.py`
**Original TODO:** `# TODO: Fix f-string missing placeholders or remove f-prefix.`

**Description:**
An f-string is used without any placeholders, which is unnecessary.

**Instructions:**
1.  Remove the `f` prefix from the string `text = f"Editor Mode..."`.
2.  Remove the TODO comment.

## 7. Implement In-Game File Dialog for Map Editor
**Location:** `command_line_conflict/scenes/editor.py`
**Original TODO:** `# TODO: Implement in-game file dialog to remove dependency on console input/Tkinter.`

**Description:**
The Map Editor falls back to console `input()` for saving and loading maps if Tkinter is not available. This disrupts the graphical user experience.

**Instructions:**
1.  Create a simple UI overlay or state in `EditorScene` to accept text input for filenames.
2.  Replace the `print()` and `input()` calls in `save_map` and `load_map` with this UI system.
3.  Remove the dependency on console interaction.
4.  Remove the TODO comment.
