# Pending Tasks

This file tracks outstanding TODOs found in the codebase and provides instructions for their resolution.

## ~~Issue 1: Create a map with factories for the player to fight against~~ (Resolved)

**Source:** ~~`command_line_conflict/factories.py:21`~~
**Context:** ~~`# TODO: Create a map with factories for the player to fight against.`~~

**Resolution:**
Implemented `FactoryBattleMap` in `command_line_conflict/maps/factory_battle_map.py` with walls,
chokepoints, and a `create_initial_units` hook that spawns player units, enemy factories
(`create_rover_factory`, `create_arachnotron_factory`), defenders, and neutral wildlife.
`GameScene` instantiates the map and delegates initial spawning via
`self.game_state.map.create_initial_units(self.game_state)`. The map is exported from
`command_line_conflict.maps` and covered by tests in
`tests/unit/maps/test_factory_battle_map.py`.
