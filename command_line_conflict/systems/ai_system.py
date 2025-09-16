from ..game_state import GameState
from ..components.position import Position
from ..components.attack import Attack
from ..components.vision import Vision
from ..components.player import Player


class AISystem:
    """Controls the behavior of AI-controlled entities."""

    def update(self, game_state: GameState) -> None:
        """Processes AI logic for all non-human entities.

        Args:
            game_state: The current state of the game.
        """
        for entity_id, components in game_state.entities.items():
            player = components.get(Player)
            if not player or player.is_human:
                continue

            attack = components.get(Attack)
            if not attack:
                continue

            # Find a target if we don't have one
            if not attack.attack_target:
                vision = components.get(Vision)
                if vision:
                    my_pos = components.get(Position)
                    if my_pos:
                        closest_enemy = self._find_closest_enemy(
                            entity_id, my_pos, player, vision, game_state
                        )
                        if closest_enemy:
                            attack.attack_target = closest_enemy

    def _find_closest_enemy(
        self,
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
