# AI Logic

The AI in Command Line Conflict is driven by the `AISystem` and supported by utility classes like `Targeting`. It is designed to be performant and capable of handling multiple units simultaneously.

## AI System

The `AISystem` (`command_line_conflict/systems/ai_system.py`) runs every frame to determine actions for computer-controlled entities.

### Logic Flow

1.  **Selection**: The system iterates efficiently over all entities possessing an `Attack` component.
2.  **Filtering**:
    *   **Dead Units**: Entities without necessary components or flagged as dead are skipped.
    *   **Neutral Units**: Units belonging to Player 0 (Neutral/Wildlife) are passive and do not auto-acquire targets unless attacked (triggered by other systems).
    *   **Existing Targets**: Units that already have a valid `attack_target` do not seek a new one until the current target is dead or out of range.
3.  **Target Acquisition**: If a unit needs a target, it invokes the `Targeting.find_closest_enemy` utility.

## Targeting Logic

The `Targeting` class (`command_line_conflict/utils/targeting.py`) provides highly optimized routines for finding enemies.

### Optimization Techniques

*   **Spatial Hashing**: Instead of iterating through all entities (O(N)), the algorithm calculates the bounding box of the unit's vision range and only checks grid cells within that area using `GameState.spatial_map`.
*   **Squared Distance Comparisons**: To avoid expensive square root calculations (`sqrt`), the system compares squared distances (`dist^2`) against the squared vision range.
    ```python
    if dist_sq <= vision_range_sq and dist_sq < min_dist_sq:
        # ...
    ```
*   **Direct Component Access**: The inner loop accesses components directly from the `GameState` dictionary to minimize function call overhead.

### Selection Criteria

A valid target must be:
1.  **Alive**: Possess a `Health` component with `hp > 0` (handled by component checks).
2.  **Enemy**: Belong to a different `Player` ID.
3.  **Visible**: Be within the `Vision` range of the seeking unit.
4.  **Closest**: The algorithm tracks the minimum squared distance to ensure the nearest threat is prioritized.
