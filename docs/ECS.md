# ECS Architecture

This project uses an **Entity-Component-System (ECS)** architecture. This pattern decouples data from logic, making the codebase more flexible, modular, and easier to test.

## Overview

```mermaid
graph TD
    subgraph Data
        E[Entity (ID)]
        C1[Component: Position]
        C2[Component: Health]
        C3[Component: Renderable]
        E --> C1
        E --> C2
        E --> C3
    end

    subgraph Logic
        S1[System: Movement]
        S2[System: Combat]
        S3[System: Rendering]
    end

    subgraph World
        GS[Game State]
    end

    GS --> E
    S1 -- Query: Position, Velocity --> E
    S2 -- Query: Position, Attack, Health --> E
    S3 -- Query: Position, Renderable --> E
```

### 1. Entities

In `Command Line Conflict`, an **Entity** is simply a unique integer ID. It has no behavior or data of its own. It serves as a key to look up components.

*   Entities are managed by the `GameState` class.
*   Example: `entity_id = game_state.create_entity()`

### 2. Components

**Components** are pure data classes. They contain no logic. They define *what* an entity is or has.

*   Located in `command_line_conflict/components/`.
*   Example:
    ```python
    @dataclass
    class Position:
        x: float
        y: float
    ```
*   If an entity has a `Position` component and a `Velocity` component, it can move. If it has `Health`, it can take damage.

### 3. Systems

**Systems** contain all the logic. They iterate over entities that possess a specific set of components and perform updates.

*   Located in `command_line_conflict/systems/`.
*   Systems are updated every frame by the `GameScene`.
*   Example: The `MovementSystem` finds all entities with both `Position` and `Movable` components and updates their `x` and `y` based on their path and speed.

### Benefits

1.  **Composition over Inheritance**: We don't need a complex class hierarchy like `Unit -> MobileUnit -> AttackingUnit`. We just mix and match components.
2.  **Performance**: Systems can optimize how they iterate over data (e.g., using spatial hashes for collision).
3.  **Decoupling**: The rendering code doesn't need to know about combat logic, only about `Position` and `Renderable` data.
