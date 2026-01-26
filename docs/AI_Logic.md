# AI Logic

The AI in `command_line_conflict` is driven by a collection of systems that manage target acquisition, movement, and self-preservation.

## Target Acquisition (`AISystem`)

The `AISystem` is responsible for finding enemies for units to attack.
- **Iteration**: It iterates over all entities with an `Attack` component.
- **Filtering**:
  - Entities belonging to Player 0 (Neutral/Nature) are ignored; they are passive.
  - Entities that already have a target are skipped.
- **Selection**: It uses `Targeting.find_closest_enemy` to locate the nearest hostile unit within vision range.
- **Heuristics**: If `Targeting` finds a valid target, it is assigned to the unit's `Attack.attack_target`.

## Movement & Pathfinding (`MovementSystem`)

The `MovementSystem` handles unit locomotion.
- **Pathfinding**: Uses the **A*** algorithm via `Map.find_path`.
- **Intelligent vs. Dumb**:
  - **Intelligent Units**: Re-calculate paths dynamically if the target moves or obstacles appear. They use a throttle (`PATH_RETRY_INTERVAL`) to prevent CPU spikes.
  - **Dumb Units**: Move in a straight line towards the target. If they collide, they stop.
- **Collision Avoidance**:
  - Units check `game_state.is_position_occupied` before moving.
  - Intelligent units exclude their destination from obstacle checks to allow moving adjacent to enemies.

## Self-Preservation (`FleeSystem`)

The `FleeSystem` overrides normal behavior when a unit is in danger.
- **Triggers**:
  - **Low Health**: If HP drops below `flee_health_threshold`.
  - **Enemy Proximity**: If `flees_from_enemies` is true and an enemy is visible.
- **Behavior**:
  - Sets `is_fleeing` flag.
  - Clears `Attack.attack_target` (flight takes priority over fight).
  - Calculates a vector away from the nearest enemy and sets a temporary movement target in the opposite direction.
- **Recovery**: If no enemies are visible and health is sufficient (or irrelevant), the unit stops fleeing and resumes normal behavior.

## Wandering (`WanderSystem`)

The `WanderSystem` provides idle behavior for neutral or patrolling units.
- **Timer**: Each unit has a `move_interval`. When the timer expires, a move is attempted.
- **Target Selection**: Picks a random coordinate within `wander_radius`.
- **Validation**: Checks if the target is walkable.
- **Execution**: Uses `Map.find_path` to generate a path to the random target, then hands off control to the `MovementSystem` via the `Movable` component.
