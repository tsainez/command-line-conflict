# Entity-Component-System (ECS) Architecture

Command Line Conflict uses an Entity-Component-System (ECS) architecture to manage game objects and their behaviors. This pattern favors composition over inheritance, allowing for greater flexibility and modularity.

## Core Concepts

*   **Entity**: A unique ID (integer) representing a game object. It has no data or behavior itself, only a collection of components.
*   **Component**: A data container holding state (e.g., `Position`, `Health`, `Renderable`). Components have no logic.
*   **System**: Logic that iterates over entities with specific components to update their state (e.g., `MovementSystem` updates `Position` based on velocity).

## Implementation Details

The core of the ECS is managed by the `GameState` class in `command_line_conflict/game_state.py`.

### Entity Storage

Entities are stored in a dictionary of dictionaries:

```python
self.entities: dict[int, dict] = {}
```

- The outer dictionary maps `entity_id` (int) to a component dictionary.
- The inner dictionary maps `ComponentType` (class) to the component instance.

This allows for O(1) access to any component of a specific entity.

### Component Indexing

To efficiently query entities by component type (e.g., "get all entities with `Health`"), `GameState` maintains an inverse index:

```python
self.component_index: dict[type, set[int]] = {}
```

- Maps `ComponentType` to a set of `entity_id`s.
- This allows O(1) retrieval of the set of entities possessing a specific component, which is crucial for Systems performance.

### Spatial Hashing

For spatial queries (e.g., "what entities are at x,y"), `GameState` uses spatial hashing:

```python
self.spatial_map: dict[tuple[int, int], set[int]] = {}
```

- Maps `(x, y)` coordinates to a set of `entity_id`s.
- This allows O(1) lookups for collision detection, targeting, and selection, avoiding O(N) iterations over all entities.
- The `Position` component automatically updates this map via `GameState` methods.

## Usage

### Creating an Entity

```python
entity_id = game_state.create_entity()
```

### Adding Components

```python
game_state.add_component(entity_id, Position(x=10, y=20))
game_state.add_component(entity_id, Health(hp=100))
```

### Querying Entities

To iterate over all entities with a specific component:

```python
for entity_id in game_state.get_entities_with_component(Health):
    health = game_state.get_component(entity_id, Health)
    # ... logic ...
```

### Spatial Queries

To get entities at a specific location:

```python
entities_at_pos = game_state.get_entities_at_position(x, y)
```
