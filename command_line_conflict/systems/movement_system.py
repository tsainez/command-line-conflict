import math

from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.unit_identity import UnitIdentity
from ..game_state import GameState
from ..logger import log


class MovementSystem:
    """Handles the movement of entities."""

    # Retry failed pathfinding after 1 second
    PATH_RETRY_INTERVAL = 1.0

    def set_target(self, game_state: GameState, entity_id: int, x: int, y: int) -> None:
        """Sets a new movement target for an entity.

        Intelligent units (e.g. rover, arachnotron) compute an A* path that
        avoids walls and other units. Non-intelligent units (e.g. chassis
        workers) skip pathfinding entirely and walk in a straight line, so
        the player must micro them around obstacles.

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
        movable.path_retry_timer = 0.0  # Reset retry timer on manual target set
        movable.stuck_notified = False  # Allow a fresh stuck-ping for the new order

        if not movable.intelligent:
            # Non-intelligent units do not pathfind. They walk in a straight
            # line; the update loop will detect collisions and ping the player.
            movable.path = []
            return

        movable.path = game_state.map.find_path(
            (int(position.x), int(position.y)),
            (x, y),
            can_fly=movable.can_fly,
            extra_obstacles=game_state.spatial_map,
            exclude_obstacles={(x, y)},
        )

        if movable.path:
            log.debug(f"Path found for entity {entity_id}: {movable.path}")
        else:
            log.warning(f"No path found for entity {entity_id} from ({position.x}, {position.y}) to ({x}, {y})")
            movable.path_retry_timer = self.PATH_RETRY_INTERVAL

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

            # Update retry timer
            if movable.path_retry_timer > 0:
                movable.path_retry_timer -= dt

            if movable.hold_position:
                movable.path = []
                movable.target_x = None
                movable.target_y = None
                continue

            # This logic is adapted from the Unit._move method
            # If intelligent and we have a target but no path, try to find one
            if not movable.path and movable.target_x is not None and movable.target_y is not None:
                if movable.intelligent:
                    # Check throttle before attempting pathfinding
                    if movable.path_retry_timer <= 0:
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
                                # Do NOT clear target here, so we can retry later.
                                # Instead, set the retry timer.
                                movable.path_retry_timer = self.PATH_RETRY_INTERVAL
                                # Previously: movable.target_x = None; movable.target_y = None
                                # Keeping target allows retrying. But we must stop motion if path is empty.
                            else:
                                # Path found!
                                pass
                    else:
                        # Throttled. Do nothing this frame regarding pathfinding.
                        pass

            if movable.path:
                next_x, next_y = movable.path[0]

                # Collision check for non-intelligent units. With the chassis
                # design they don't have paths anymore, but keep the guard so
                # any external system that sets a path (e.g. wander) still
                # produces a stuck-ping rather than silently clipping.
                if not movable.intelligent:
                    # Optimized: Use is_position_occupied to avoid list allocation
                    if game_state.is_position_occupied(next_x, next_y, exclude_entity_id=entity_id):
                        log.debug(f"Collision detected for non-intelligent entity {entity_id} at ({next_x}, {next_y})")
                        self._notify_stuck(game_state, entity_id, blocked_by_wall=False, blocked_by_unit=True)
                        movable.path = []
                        movable.target_x = None
                        movable.target_y = None
                        continue

                movable.target_x, movable.target_y = next_x, next_y
                dx = movable.target_x - position.x
                dy = movable.target_y - position.y

                # Optimization: Compare squared distance to avoid expensive sqrt() when unit has arrived
                dist_sq = dx * dx + dy * dy
                if dist_sq < 0.0001:
                    game_state.update_entity_position(entity_id, movable.target_x, movable.target_y)
                    movable.path.pop(0)
                else:
                    dist = math.sqrt(dist_sq)

                    # Optimization: Pre-calculate the ratio to avoid dividing x and y coordinates twice
                    step_ratio = min(movable.speed * dt, dist) / dist
                    new_x = position.x + step_ratio * dx
                    new_y = position.y + step_ratio * dy

                    game_state.update_entity_position(entity_id, new_x, new_y)

            # Fallback for simple movement if pathfinding is not used or empty
            # BUT: If intelligent and path is empty, it means we have no path.
            # If target is set but path is empty, it means we failed pathfinding (throttled)
            # or we are at the target?

            # Original code had:
            # elif movable.target_x is not None and movable.target_y is not None:

            # If intelligent is True, we ONLY move via path.
            # If intelligent is False, we move via direct line.

            elif not movable.intelligent and movable.target_x is not None and movable.target_y is not None:
                dx = movable.target_x - position.x
                dy = movable.target_y - position.y

                # Optimization: Compare squared distance to avoid expensive sqrt() when unit has arrived
                dist_sq = dx * dx + dy * dy
                if dist_sq < 0.0001:
                    # The unit has effectively arrived. If the target tile
                    # itself is blocked we're stuck on the destination, not
                    # mid-route, so ping the player here too.
                    tix, tiy = int(movable.target_x), int(movable.target_y)
                    arrived_blocked_wall = not movable.can_fly and not game_state.map.is_walkable(tix, tiy)
                    arrived_blocked_unit = (not arrived_blocked_wall) and game_state.is_position_occupied(
                        tix, tiy, exclude_entity_id=entity_id
                    )
                    if arrived_blocked_wall or arrived_blocked_unit:
                        log.debug(f"Collision detected for non-intelligent entity {entity_id} " f"at target ({tix}, {tiy})")
                        self._notify_stuck(game_state, entity_id, arrived_blocked_wall, arrived_blocked_unit)
                    movable.target_x = None
                    movable.target_y = None
                    continue

                dist = math.sqrt(dist_sq)

                # Optimization: Pre-calculate the ratio to avoid dividing x and y coordinates twice
                step_ratio = min(movable.speed * dt, dist) / dist

                proposed_x = position.x + step_ratio * dx
                proposed_y = position.y + step_ratio * dy

                pix, piy = int(proposed_x), int(proposed_y)

                blocked_by_wall = not movable.can_fly and not game_state.map.is_walkable(pix, piy)
                blocked_by_unit = (not blocked_by_wall) and game_state.is_position_occupied(
                    pix, piy, exclude_entity_id=entity_id
                )

                if blocked_by_wall or blocked_by_unit:
                    log.debug(f"Collision detected for non-intelligent entity {entity_id} at ({proposed_x}, {proposed_y})")
                    self._notify_stuck(game_state, entity_id, blocked_by_wall, blocked_by_unit)
                    movable.target_x = None
                    movable.target_y = None
                    continue

                game_state.update_entity_position(entity_id, proposed_x, proposed_y)

    def _notify_stuck(
        self,
        game_state: GameState,
        entity_id: int,
        blocked_by_wall: bool,
        blocked_by_unit: bool,
    ) -> None:
        """Pings the player that one of their non-intelligent units is stuck.

        Emits a single log event per stuck order so the chat/log overlay shows
        a notification. Non-human owners (AI, neutral wildlife) are silenced.
        """
        components = game_state.entities.get(entity_id)
        if not components:
            return

        movable = components.get(Movable)
        if movable is None or movable.stuck_notified:
            return

        player = components.get(Player)
        if not player or not player.is_human:
            movable.stuck_notified = True
            return

        identity = components.get(UnitIdentity)
        unit_label = identity.name.capitalize() if identity else f"Unit {entity_id}"

        if blocked_by_wall and blocked_by_unit:
            text = f"{unit_label} is stuck!"
        elif blocked_by_wall:
            text = f"{unit_label} is blocked by terrain!"
        else:
            text = f"{unit_label} is blocked by another unit!"

        game_state.add_event({"type": "log", "text": text, "color": (255, 200, 50)})
        movable.stuck_notified = True
