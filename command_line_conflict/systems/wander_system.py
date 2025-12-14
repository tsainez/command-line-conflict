import random

from ..components.movable import Movable
from ..components.position import Position
from ..components.wander import Wander
from ..game_state import GameState


class WanderSystem:
    """Controls the random movement of entities with the Wander component."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes wandering logic.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in game_state.entities.items():
            wander = components.get(Wander)
            movable = components.get(Movable)
            position = components.get(Position)

            if not wander or not movable or not position:
                continue

            # Check if currently moving
            if movable.path or (movable.target_x is not None):
                continue

            # Update timer
            wander.time_since_last_move += dt

            if wander.time_since_last_move >= wander.move_interval:
                # Pick a random target
                dx = random.randint(-wander.wander_radius, wander.wander_radius)
                dy = random.randint(-wander.wander_radius, wander.wander_radius)

                target_x = int(position.x + dx)
                target_y = int(position.y + dy)

                # Clamp to map bounds
                target_x = max(0, min(target_x, game_state.map.width - 1))
                target_y = max(0, min(target_y, game_state.map.height - 1))

                # Simple check if target is valid (not a wall)
                if game_state.map.is_walkable(target_x, target_y):
                    # Use MovementSystem logic indirectly by setting path (or relying on MovementSystem to calculate it)
                    # But MovementSystem.set_target is a method on the system instance, not available here easily
                    # unless we pass the system or duplicate logic.
                    # However, Movable component has target_x/target_y which MovementSystem reads.
                    # But MovementSystem usually calculates path *once* in set_target.
                    # If we just set target_x/y, MovementSystem might just move in straight line.
                    # Let's use game_state.map.find_path here to be safe and set the path.

                    path = game_state.map.find_path(
                        (int(position.x), int(position.y)),
                        (target_x, target_y),
                        can_fly=movable.can_fly,
                    )

                    if path:
                        movable.path = path
                        movable.target_x = path[0][0]
                        movable.target_y = path[0][1]
                        wander.time_since_last_move = 0.0
