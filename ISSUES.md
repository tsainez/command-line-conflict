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
