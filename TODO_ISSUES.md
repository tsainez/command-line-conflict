# Pending Tasks

This file tracks outstanding TODOs found in the codebase and provides instructions for their resolution.

## Issue 1: Create a map with factories for the player to fight against

**Source:** `command_line_conflict/factories.py:21`
**Context:** `# TODO: Create a map with factories for the player to fight against.`

**Description:**
The codebase currently relies on `GameScene._create_initial_units` to spawn entities, and uses a `SimpleMap` (empty map). To support more complex gameplay, specifically a scenario where the player fights against enemy factories, a dedicated map configuration or subclass is needed.

**Instructions:**
1.  **Create a New Map Class:**
    *   Create a new file `command_line_conflict/maps/factory_battle_map.py`.
    *   Define a class `FactoryBattleMap` inheriting from `Map`.
    *   Initialize it with appropriate dimensions and walls (optional).
2.  **Refactor GameScene for Map-Specific Spawning:**
    *   Modify `GameScene.__init__` to accept a map instance or factory, or determine the map based on `current_mission_id`.
    *   Modify `GameScene._create_initial_units` to delegate unit spawning to the map instance (e.g., `self.game_state.map.create_initial_units(self.game_state)`), OR create a new `Mission` class that bundles the Map and the initial unit spawning logic.
3.  **Implement the Factory Battle Scenario:**
    *   In the new spawning logic (in the Map or Mission):
        *   Spawn player units (e.g., Chassis, Rovers).
        *   Spawn enemy factories (`create_rover_factory`, `create_arachnotron_factory`) at strategic locations.
        *   Ensure enemy factories have defensive units nearby.
4.  **Cleanup:**
    *   Remove the TODO comment from `command_line_conflict/factories.py`.
