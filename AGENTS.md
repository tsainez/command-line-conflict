# AGENTS.md

## Agent Instructions
Before creating a Pull Request, you **must** run the pre-commit script to verify your changes:
```bash
./scripts/pre_commit.sh
```
All checks (formatting, linting, testing) must pass.

This file contains a backlog of 100 potential tasks that can be performed by autonomous coding agents to improve the `command_line_conflict` project.

## Features / Gameplay
1. Implement fog of war smoothing for better visual transitions.
2. Add a minimap to the HUD.
3. [x] Implement A* pathfinding for unit movement.
4. [x] Add different unit types (Melee, Ranged, Flying).
5. Implement resource gathering animations (ASCII characters changing).
6. Add building construction timers and animations.
7. [x] Implement a tech tree system for unlocking units.
8. Add weapon and armor upgrade systems.
9. Implement Hero units with special abilities.
10. [x] Add neutral creeps/wildlife to maps.
11. [x] Implement day/night cycle with visual effects (dimming).
12. Add weather effects like rain or snow (overlay characters).
13. Implement different terrain types (slow movement, high ground bonus).
14. Add destructible rocks/obstacles.
15. Implement unit control groups (0-9 keys).
16. [x] Add hotkeys for building construction and unit training.
17. [x] Implement game pause functionality.
18. [x] Add save/load game functionality during a mission.
19. Implement a replay system to watch past games.
20. Add an observer mode for spectating.
21. [x] Implement an in-game chat/log system.
22. [x] Add cheat codes for testing (e.g., reveal map, infinite resources).
23. Implement selectable difficulty levels.
24. Add a scripted tutorial mission.
25. [x] Implement a campaign progression map screen.
26. Add ASCII art cutscenes between missions.
27. [x] Implement sound effect hooks (even if silent initially).
28. [x] Add background music support.
29. [x] Implement a main menu with configurable options.
30. [x] Add keybinding configuration menu.
31. [x] Implement screen resolution or text size scaling.
32. [x] Add unit health bars/indicators.
33. Implement unit energy/mana for abilities.
34. Add cooldown management for abilities.
35. [x] Implement "Hold Position" command.
36. Implement "Patrol" command.
37. Implement "Attack Move" command.
38. Add unit formations.
39. Implement collision avoidance between friendly units.
40. Add floating combat text (damage numbers).

## AI / Bot
41. Create a basic "Random Move" AI.
42. Create a dedicated Resource Gathering AI.
43. Create a "Rush" strategy AI (early aggression).
44. Create a "Turtle" strategy AI (defensive).
45. Implement AI personality or chat taunts.
46. Add AI difficulty scaling (limit APM or resource rates).
47. Implement AI scouting behavior.
48. [x] Create AI logic to retreat when units are low health.
49. Implement AI base expansion logic.
50. Create a Reinforcement Learning gym wrapper for the game.

## Architecture / Refactoring
51. Refactor ECS storage to be more cache-friendly.
52. Split the large `engine.py` into smaller, focused modules.
53. Introduce an Event Bus for decoupled system communication.
54. Optimize the rendering loop to reduce flicker.
55. Add comprehensive type hinting to the entire codebase.
56. [x] Add docstrings to all public functions and classes.
57. [x] Refactor map loading to use a standard format like JSON or YAML.
58. Implement a Dependency Injection container.
59. Extract all hardcoded configuration values to a separate config file.
60. [x] Create a unified logging system with different levels.
61. Refactor unit logic into a State Machine pattern.
62. Optimize collision detection using a Quadtree or spatial hash.
63. Refactor input handling to support custom keymaps easily.
64. Abstract the rendering interface to allow potential GUI backends.
65. Implement object pooling for frequently created entities (units/projectiles).
66. [x] Refactor the Factory pattern for entity creation.
67. Standardize error handling and exceptions.
68. Remove magic numbers and replace with named constants.
69. [x] Enforce PEP8 compliance across the codebase.
70. [x] Sort imports automatically using `isort` configuration.

## Testing / QA
71. Add unit tests for the core `Game` class.
72. Add integration tests for full campaign mission flow.
73. Implement property-based testing using `Hypothesis`.
74. Add performance benchmarks for the game loop.
75. Implement fuzz testing for input handling.
76. Add visual regression tests (comparing screen output snapshots).
77. Create a stress test spawning 1000 units to check stability.
78. [x] Add test coverage reporting (target > 80%).
79. [x] Implement automated map validation (check for unreachable areas).
80. [x] Add static analysis (pylint, mypy) checks to the pipeline.
81. Create test fixtures for complex game scenarios (e.g., max supply).
82. [x] Mock external dependencies (like Pygame) effectively in tests.
83. [x] Add pre-commit hooks for linting and formatting.
84. Verify determinism in game logic (same seed = same outcome).
85. Test backward compatibility of save files.

## Documentation
86. [x] Create a `CONTRIBUTING.md` file with guidelines.
87. Document the ECS architecture with a diagram.
88. Create API documentation using Sphinx or MkDocs.
89. Write a guide on "How to Create a New Map".
90. [x] Document available cheat codes and debug commands.
91. Create a changelog generation script.
92. Write a "Getting Started" guide for new developers.
93. Document known issues and workarounds.
94. Create an ASCII art style guide for the game.
95. Document AI behavior trees and logic flow.

## DevOps / Tooling
96. Create a Dockerfile for running the game in a container.
97. [x] Set up GitHub Actions for Continuous Integration.
98. [x] Create a release script to package the game.
99. Add a "watch mode" script for auto-restarting on code changes.
100. [x] Create a map editor tool (CLI or simple GUI).
