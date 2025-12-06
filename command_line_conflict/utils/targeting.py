from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..game_state import GameState

# TODO: Integrate logger for debug mode. Currently not used.


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

        Args:
            my_id: The ID of the searching entity.
            my_pos: The position component of the searching entity.
            my_player: The player component of the searching entity.
            vision: The vision component of the searching entity.
            game_state: The current game state.

        Returns:
            int | None: The ID of the closest enemy entity, or None if no enemy is found.
        """
        closest_enemy = None
        min_dist = float("inf")

        for other_id, other_components in game_state.entities.items():
            if other_id == my_id:
                continue

            other_player = other_components.get(Player)
            if not other_player or other_player.player_id == my_player.player_id:
                continue

            other_pos = other_components.get(Position)
            if not other_pos:
                continue

            dist = (
                (my_pos.x - other_pos.x) ** 2 + (my_pos.y - other_pos.y) ** 2
            ) ** 0.5
            if dist <= vision.vision_range and dist < min_dist:
                min_dist = dist
                closest_enemy = other_id
        return closest_enemy
