# ECS Architecture

The Entity-Component-System (ECS) is the core architectural pattern used in `command_line_conflict`. It decouples data from behavior, allowing for a flexible and performant game engine.

## Overview Diagram

```mermaid
classDiagram
    class GameState {
        +dict entities
        +dict components
        +SpatialHash spatial_map
        +list event_queue
        +add_entity()
        +get_entities_with_component()
    }

    class Entity {
        +int id
    }

    class Component {
        <<Data>>
    }
    class Position {
        +float x
        +float y
    }
    class Velocity {
        +float dx
        +float dy
    }
    class Health {
        +int current
        +int max
    }

    class System {
        <<Logic>>
        +update(game_state, dt)
    }
    class MovementSystem {
        +update()
    }
    class RenderingSystem {
        +draw()
    }
    class CombatSystem {
        +update()
    }

    GameState *-- Entity : Manages
    GameState *-- Component : Stores
    Entity "1" o-- "n" Component : Has
    Component <|-- Position
    Component <|-- Velocity
    Component <|-- Health

    System ..> GameState : Reads/Writes
    MovementSystem --|> System
    RenderingSystem --|> System
    CombatSystem --|> System
```

## Core Concepts

### 1. Entities
An **Entity** is just a unique integer ID. It has no behavior or data of its own. It serves as a key to associate different components together.

### 2. Components
A **Component** is a pure data class. It contains no logic.
*   **Position**: Where an object is.
*   **Renderable**: What an object looks like.
*   **Health**: How much damage an object can take.

### 3. Systems
A **System** contains the logic. It iterates over entities that have a specific set of components and performs operations on them.
*   **MovementSystem**: Iterates over entities with `Position` and `Velocity` and updates `Position` based on `Velocity` * `dt`.
*   **CombatSystem**: Iterates over entities with `Attack` and checks for targets within range.

### 4. GameState
The **GameState** is the central database. It holds:
*   All entities (IDs).
*   All components (mapped by Entity ID).
*   A spatial index (Spatial Hash) for fast position-based lookups.
*   An event queue for inter-system communication (e.g., "Unit Died", "Sound Played").
