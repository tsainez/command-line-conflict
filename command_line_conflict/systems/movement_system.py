from ..game_state import GameState
from ..components.position import Position
from ..components.movable import Movable


class MovementSystem:
    """Handles the movement of entities."""

    def set_target(self, game_state: GameState, entity_id: int, x: int, y: int) -> None:
        """Sets a new movement target for an entity and calculates the path.

        Args:
            game_state: The current state of the game.
            entity_id: The ID of the entity to move.
            x: The target x-coordinate.
            y: The target y-coordinate.
        """
        movable = game_state.get_component(entity_id, Movable)
        position = game_state.get_component(entity_id, Position)
        if not movable or not position:
            return

        movable.target_x = x
        movable.target_y = y
        movable.path = game_state.map.find_path(
            (int(position.x), int(position.y)),
            (x, y),
            can_fly=movable.can_fly,
        )

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes entity movement based on their current path or target.

        This method moves entities along their calculated path or directly
        towards their target if no path is set.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in game_state.entities.items():
            position = components.get(Position)
            movable = components.get(Movable)

            if not position or not movable:
                continue

            # This logic is adapted from the Unit._move method
            if movable.path:
                next_x, next_y = movable.path[0]
                # In the future, we'll need to handle pathfinding and obstacles.
                # For now, we'll just move towards the next point in the path.

                movable.target_x, movable.target_y = next_x, next_y
                dx = movable.target_x - position.x
                dy = movable.target_y - position.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 0.01:
                    position.x = movable.target_x
                    position.y = movable.target_y
                    movable.path.pop(0)
                else:
                    step = movable.speed * dt
                    if step > dist:
                        step = dist
                    position.x += step * dx / dist
                    position.y += step * dy / dist
            elif movable.target_x is not None and movable.target_y is not None:
                dx = movable.target_x - position.x
                dy = movable.target_y - position.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 0.01:
                    continue

                step = movable.speed * dt
                if step > dist:
                    step = dist

                proposed_x = position.x + step * dx / dist
                proposed_y = position.y + step * dy / dist

                # In the future, we'll need to handle collision detection.
                # For now, we'll just move to the proposed position.

                position.x = proposed_x
                position.y = proposed_y
