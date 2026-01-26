# ECS Architecture

The `command_line_conflict` engine is built on an **Entity-Component-System (ECS)** architecture. This pattern favors composition over inheritance, allowing for flexible and performant game entities.

## Core Concepts

### GameState
The `GameState` class (`command_line_conflict/game_state.py`) is the central hub of the simulation. It manages:
- **Entities**: Stored as a dictionary of dictionaries (`{entity_id: {ComponentType: ComponentInstance}}`).
- **Components**: Data containers attached to entities.
- **Systems**: Logic processors that operate on entities with specific components.
- **Events**: A queue for decoupled communication (e.g., between combat logic and UI feedback).

### Entities
Entities are simply unique Integer IDs. They have no data or behavior themselves; they are defined entirely by the components attached to them.

### Components
Components are pure data classes. They contain state but no logic. Examples include:
- `Position`: Stores x, y coordinates.
- `Health`: Stores current and max HP.
- `Movable`: Stores speed, target destination, and pathfinding state.
- `Attack`: Stores damage, range, and current target.

### Systems
Systems contain the game logic. They iterate over entities that possess a specific set of components and update their state.
- `MovementSystem`: Updates `Position` based on `Movable` data.
- `AISystem`: Updates `Attack` targets based on `Vision` and proximity.
- `RenderingSystem`: Draws entities based on `Position` and `Renderable` components.

## Performance Optimizations

To ensure the game runs smoothly even with many units, the `GameState` implements several optimizations:

### Component Indexing
Instead of iterating over all entities to find those with a specific component (O(N)), `GameState` maintains a `component_index`:
```python
self.component_index: dict[type, set[int]]
```
This allows systems to retrieve relevant entities in O(1) time (or O(S) where S is the number of matching entities).

### Spatial Hashing
For spatial queries (e.g., "what units are at position (x, y)?"), iterating all entities would be too slow. `GameState` uses a spatial hash map:
```python
self.spatial_map: dict[tuple[int, int], set[int]]
```
This allows:
- **O(1)** collision detection.
- **O(1)** unit selection by click.
- Efficient range checks for vision and combat.

## Event System
The `GameState` maintains an `event_queue`. Systems can emit events (e.g., `visual_effect`) which are consumed by other systems (like `UISystem`) later in the frame. This prevents tight coupling between simulation logic and presentation logic.
