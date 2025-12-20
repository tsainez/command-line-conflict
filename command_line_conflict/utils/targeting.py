from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..config import DEBUG
from ..game_state import GameState
from ..logger import log


class Targeting:
    """A utility class for targeting logic."""

    @staticmethod
    def find_closest_enemy(
        my_id: int,
        my_pos: Position,
        my_player: Player,
        vision: Vision,
        game_state: GameState,
    ) -> int | None:
        """Finds the closest enemy entity within the vision range.

        Optimized to use spatial hashing to avoid O(N) iteration over all entities.
        """
        if DEBUG:
            log.debug(f"Targeting: Searching for enemy for unit {my_id} at ({my_pos.x}, {my_pos.y})")

        closest_enemy = None
        min_dist = float("inf")
        vision_range = vision.vision_range

        # Calculate search bounds based on vision range
        min_x = int(my_pos.x - vision_range)
        max_x = int(my_pos.x + vision_range)
        min_y = int(my_pos.y - vision_range)
        max_y = int(my_pos.y + vision_range)

        # Iterate only over the grid cells within the vision range
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # Retrieve potential targets from the spatial map
                cell_entities = game_state.spatial_map.get((x, y))
                if not cell_entities:
                    continue

                for other_id in cell_entities:
                    if other_id == my_id:
                        continue

                    # Retrieve components directly for performance
                    other_components = game_state.entities.get(other_id)
                    if not other_components:
                        continue

                    other_player = other_components.get(Player)
                    if not other_player or other_player.player_id == my_player.player_id:
                        continue

                    other_pos = other_components.get(Position)
                    if not other_pos:
                        continue

                    dist = ((my_pos.x - other_pos.x) ** 2 + (my_pos.y - other_pos.y) ** 2) ** 0.5

                    if dist <= vision_range and dist < min_dist:
                        min_dist = dist
                        closest_enemy = other_id

        if DEBUG and closest_enemy:
            log.debug(f"Targeting: Found target {closest_enemy} for unit {my_id} at distance {min_dist:.2f}")

        return closest_enemy
