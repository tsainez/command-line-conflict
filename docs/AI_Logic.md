# AI and Movement Logic

This document describes the internal logic for the AI decision-making and unit movement systems in **Command Line Conflict**.

## AI System

The `AISystem` (`command_line_conflict/systems/ai_system.py`) is responsible for high-level decision making for units, specifically target acquisition.

### Target Acquisition

1.  **Iterate Attackers**: The system iterates over all entities with an `Attack` component.
2.  **Filter**:
    *   Entities must have a `Player` component.
    *   Entities belonging to Player 0 (Neutral) are ignored.
    *   Entities that already have an `attack_target` are skipped.
3.  **Find Target**:
    *   If the entity has a `Vision` component, it looks for the closest enemy.
    *   It uses `Targeting.find_closest_enemy` to scan for potential targets within vision range.
    *   If a target is found, `attack.attack_target` is set.

## Movement System

The `MovementSystem` (`command_line_conflict/systems/movement_system.py`) handles unit locomotion, pathfinding, and collision avoidance.

### Pathfinding (A*)

Movement uses the A* algorithm implemented in `Map.find_path` (`command_line_conflict/maps/base.py`).

*   **Heuristic**: Manhattan distance (`|dx| + |dy|`).
*   **Grid**: The map is treated as a grid where movement is allowed in 4 directions (Up, Down, Left, Right).
*   **Obstacles**: Walls block movement unless the unit `can_fly`.
*   **Dynamic Obstacles**: The system can account for temporary obstacles (like other units) using `extra_obstacles`.

### Movement Logic

1.  **Target Setting**: When a command is issued, `set_target` calculates a path using A*.
2.  **Path Following**: In `update()`, the unit moves towards the next node in its `path`.
3.  **Intelligent vs. Simple**:
    *   **Intelligent** units (e.g., player units) recalculate paths if blocked and use full A*.
    *   **Simple** units (e.g., projectiles) move in a straight line and stop on collision.
4.  **Collision Avoidance**:
    *   Units check `is_position_occupied` before moving into a cell.
    *   If a path is blocked, intelligent units try to repath (throttled by `PATH_RETRY_INTERVAL`).

### Flowchart (Textual)

```text
[Unit] -> Has Target?
   |
   +-> No -> Stay Idle / Hold Position
   |
   +-> Yes -> Has Path?
         |
         +-> Yes -> Move to Next Step -> Collision?
         |             |
         |             +-> No -> Update Position
         |             |
         |             +-> Yes -> Recalculate Path
         |
         +-> No -> Calculate A* Path -> Found?
                     |
                     +-> Yes -> Store Path
                     |
                     +-> No -> Wait / Retry later
```
