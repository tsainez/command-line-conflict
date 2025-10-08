from ..components.player import Player
from ..components.position import Position
from ..components.resource import Resource
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
        """Finds the closest enemy entity within the vision range."""
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

    @staticmethod
    def find_closest_minerals(
        my_id: int, my_pos: Position, vision: Vision, game_state: GameState
    ) -> int | None:
        """Finds the closest mineral patch within the vision range."""
        closest_minerals = None
        min_dist = float("inf")

        for other_id, other_components in game_state.entities.items():
            if other_id == my_id:
                continue

            if not other_components.get(Resource):
                continue

            other_pos = other_components.get(Position)
            if not other_pos:
                continue

            dist = (
                (my_pos.x - other_pos.x) ** 2 + (my_pos.y - other_pos.y) ** 2
            ) ** 0.5
            if dist <= vision.vision_range and dist < min_dist:
                min_dist = dist
                closest_minerals = other_id
        return closest_minerals
