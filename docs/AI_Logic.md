# AI Logic

This document describes the behavior of the AI systems in **Command Line Conflict**.

## Overview

The AI is driven by several ECS systems that operate independently on entities with specific components. The main logic is handled by `AISystem`, but `WanderSystem` and `FleeSystem` also contribute to unit behavior.

## Core Systems

### 1. AISystem (Combat & Targeting)

The `AISystem` is responsible for enemy engagement.

*   **Target Acquisition**: Entities with an `Attack` component and a `Player` component will automatically scan for enemies.
    *   **Requirements**: The unit must have a `Vision` component to "see" enemies.
    *   **Logic**: It uses `Targeting.find_closest_enemy` to locate the nearest hostile unit within vision range.
    *   **Auto-Attack**: Once a target is acquired, the `Attack` component's `attack_target` field is set, and the `CombatSystem` takes over to handle the actual attacking.
*   **Neutral Units**: Entities belonging to Player 0 (Neutral/Wildlife) are treated as passive by the `AISystem`. They do not actively seek targets, although they may defend themselves if attacked (depending on `CombatSystem` logic).

### 2. WanderSystem (Idle Movement)

The `WanderSystem` controls the idle movement of units, primarily used for wildlife.

*   **Components**: Requires the `Wander` component.
*   **Behavior**: Units will pick a random valid location within their `wander_radius` and move there at intervals defined by `move_interval`.

### 3. FleeSystem (Retreat)

The `FleeSystem` overrides normal movement to make units run away from threats.

*   **Triggers**:
    *   **Health Threshold**: If an entity's health drops below a certain percentage (defined in the `Flee` component), it will flee.
    *   **Always Flee**: Some units (like the Observer) are configured to always flee from enemies regardless of health.
*   **Behavior**: The system calculates a vector away from the nearest enemy and sets the movement target to a safe distance in that direction.

## Unit Specific Behaviors

*   **Wildlife**: Uses `WanderSystem` to roam. Passive unless attacked.
*   **Combat Units (Rover, Arachnotron, etc.)**: Use `AISystem` to hunt enemies.
*   **Observer**: Uses `FleeSystem` to avoid combat, as it has no attack capability.
