# Issues Identified from TODOs

## ~~1. Implement Factory Map for Gameplay~~ (Resolved)
**Location:** ~~`command_line_conflict/factories.py`~~
**Original TODO:** ~~`# TODO: Create a map with factories for the player to fight against.`~~

**Resolution:**
~~The game currently lacks a map specifically designed for player vs factory combat.~~
Implemented as `FactoryBattleMap` in `command_line_conflict/maps/factory_battle_map.py`.
The map defines a 60x40 arena with chokepoint walls and provides a
`create_initial_units` hook that spawns the human player's starting units along with
enemy factories and defenders. `GameScene` now uses this map and delegates initial
spawning to it. The map is exported from `command_line_conflict.maps` and covered by
unit tests.

**Instructions:** ~~All steps completed; TODO comment already removed from `factories.py`.~~

## 3. Remove Unused Imports
**Locations:**
*   ~~`command_line_conflict/engine.py`~~
*   ~~`command_line_conflict/systems/combat_system.py`~~
*   ~~`command_line_conflict/systems/selection_system.py`~~
*   ~~`command_line_conflict/systems/ui_system.py`~~

**Original TODOs:**
*   `# TODO: Remove unused import.`

**Description:**
Several files contain unused imports which clutter the code and can be confusing.

**Instructions:**
1.  ~~Remove `import os` from `command_line_conflict/engine.py`.~~
2.  ~~Remove `Player` and `Vision` imports from `command_line_conflict/systems/combat_system.py` if they are indeed unused.~~
3.  ~~Remove `config` import from `command_line_conflict/systems/selection_system.py`.~~
4.  ~~Remove `import math` from `command_line_conflict/systems/ui_system.py`.~~
5.  ~~Remove the corresponding TODO comments.~~

## 6. Fix F-string in Editor Scene
**Location:** ~~`command_line_conflict/scenes/editor.py`~~
**Original TODO:** ~~`# TODO: Fix f-string missing placeholders or remove f-prefix.`~~

**Description:**
~~An f-string is used without any placeholders, which is unnecessary.~~

**Instructions:**
1.  ~~Remove the `f` prefix from the string `text = f"Editor Mode..."`.~~
2.  ~~Remove the TODO comment.~~

