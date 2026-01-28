# ECS Architecture

Command Line Conflict uses an **Entity-Component-System (ECS)** architecture to manage game objects and logic. This pattern decouples data from behavior, making the codebase more modular and easier to extend.

## Overview

The core concept is that game objects are not monolithic classes but rather aggregations of data components. Systems then operate on entities that possess specific components.

```mermaid
graph TD
    subgraph "Core"
        GameLoop[Game Loop] -->|Updates| GameState
        GameState -->|Contains| EntityManager
        GameState -->|Contains| SystemManager
    end

    subgraph "Data"
        EntityManager -->|Manages| Entity
        Entity -->|Has| Component
        Component -->|Stores| Data[Pure Data]
    end

    subgraph "Logic"
        SystemManager -->|Runs| System
        System -->|Queries| EntityManager
        System -->|Updates| Component
    end
```

## Concepts

### Entity

An **Entity** is just a unique ID (an integer). It doesn't hold any data or logic itself. It's merely a key to look up components.

In `command_line_conflict`, an Entity is represented by an `int`.

### Component

A **Component** is a pure data class. It contains state but no logic.

Examples:
- `PositionComponent`: Stores `x` and `y` coordinates.
- `HealthComponent`: Stores `current_hp` and `max_hp`.
- `RenderableComponent`: Stores the ASCII character and color.

### System

A **System** contains logic. It iterates over all entities that have a specific set of components and performs actions on them.

Examples:
- `MovementSystem`: Iterates over entities with `Position` and `Velocity`. Updates `Position` based on `Velocity`.
- `RenderingSystem`: Iterates over entities with `Position` and `Renderable`. Draws them to the screen.

## Benefits

1.  **Decoupling**: You can add new behavior (System) without modifying the data (Component) or the object (Entity).
2.  **Performance**: Systems operate on flat arrays of data, which can be optimized for cache locality (though Python implementation is less strict about this).
3.  **Composition over Inheritance**: You can create complex objects by mixing and matching simple components.

## Implementation Details

The core ECS logic resides in `command_line_conflict/game_state.py`.
- `GameState` acts as the world container.
- `get_entities_with_component(*component_types)` is the primary way Systems query for entities.
