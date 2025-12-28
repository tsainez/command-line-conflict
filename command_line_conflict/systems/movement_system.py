from ..components.movable import Movable
from ..components.position import Position
from ..game_state import GameState
from ..logger import log


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
            log.warning(f"Missing components for entity {entity_id}: Movable={bool(movable)}, Position={bool(position)}")
            return

        log.debug(f"Setting target for entity {entity_id} from ({position.x}, {position.y}) to ({x}, {y})")

        movable.target_x = x
        movable.target_y = y

        extra_obstacles = None
        exclude_obstacles = None
        if movable.intelligent:
            extra_obstacles = game_state.spatial_map
            exclude_obstacles = {(x, y)}

        movable.path = game_state.map.find_path(
            (int(position.x), int(position.y)),
            (x, y),
            can_fly=movable.can_fly,
            extra_obstacles=extra_obstacles,
            exclude_obstacles=exclude_obstacles,
        )

        if movable.path:
            log.debug(f"Path found for entity {entity_id}: {movable.path}")
        else:
            log.warning(f"No path found for entity {entity_id} from ({position.x}, {position.y}) to ({x}, {y})")

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes entity movement based on their current path or target.

        This method moves entities along their calculated path or directly
        towards their target if no path is set.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        # Optimized to iterate only over entities with Movable component
        for entity_id in game_state.get_entities_with_component(Movable):
            components = game_state.entities.get(entity_id)
            if not components:
                continue

            position = components.get(Position)
            movable = components.get(Movable)

            if not position or not movable:
                continue

            if movable.hold_position:
                movable.path = []
                movable.target_x = None
                movable.target_y = None
                continue

            # This logic is adapted from the Unit._move method
            # If intelligent and we have a target but no path, try to find one
            if not movable.path and movable.target_x is not None and movable.target_y is not None:
                if movable.intelligent:
                    start_node = (int(position.x), int(position.y))
                    end_node = (int(movable.target_x), int(movable.target_y))
                    if start_node != end_node:
                        # Use spatial map directly and exclude the target
                        extra_obstacles = game_state.spatial_map
                        exclude_obstacles = {end_node}

                        movable.path = game_state.map.find_path(
                            start_node,
                            end_node,
                            can_fly=movable.can_fly,
                            extra_obstacles=extra_obstacles,
                            exclude_obstacles=exclude_obstacles,
                        )
                        if not movable.path:
                            # No path found to target, stop to avoid clipping
                            log.warning(
                                f"Intelligent pathfinding failed for entity {entity_id} "
                                f"to ({movable.target_x}, {movable.target_y})"
                            )
                            movable.target_x = None
                            movable.target_y = None

            if movable.path:
                next_x, next_y = movable.path[0]

                # Collision check for non-intelligent units
                if not movable.intelligent:
                    entities_at_next_pos = game_state.get_entities_at_position(next_x, next_y)
                    if any(e != entity_id for e in entities_at_next_pos):
                        log.debug(f"Collision detected for non-intelligent entity {entity_id} at ({next_x}, {next_y})")
                        movable.path = []
                        movable.target_x = None
                        movable.target_y = None
                        continue

                movable.target_x, movable.target_y = next_x, next_y
                dx = movable.target_x - position.x
                dy = movable.target_y - position.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 0.01:
                    game_state.update_entity_position(entity_id, movable.target_x, movable.target_y)
                    movable.path.pop(0)
                else:
                    step = min(movable.speed * dt, dist)
                    new_x = position.x + step * dx / dist
                    new_y = position.y + step * dy / dist
                    game_state.update_entity_position(entity_id, new_x, new_y)
            elif movable.target_x is not None and movable.target_y is not None:
                dx = movable.target_x - position.x
                dy = movable.target_y - position.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 0.01:
                    continue

                step = min(movable.speed * dt, dist)

                proposed_x = position.x + step * dx / dist
                proposed_y = position.y + step * dy / dist

                # Collision check for non-intelligent units
                if not movable.intelligent:
                    entities_at_proposed_pos = game_state.get_entities_at_position(int(proposed_x), int(proposed_y))
                    if any(e != entity_id for e in entities_at_proposed_pos):
                        log.debug(f"Collision detected for non-intelligent entity {entity_id} at ({proposed_x}, {proposed_y})")
                        movable.target_x = None
                        movable.target_y = None
                        continue

                game_state.update_entity_position(entity_id, proposed_x, proposed_y)
