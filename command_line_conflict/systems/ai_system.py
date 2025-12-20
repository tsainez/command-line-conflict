from ..components.attack import Attack
from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..game_state import GameState
from ..logger import log
from ..utils.targeting import Targeting


class AISystem:
    """Controls the behavior of AI-controlled entities."""

    def update(self, game_state: GameState) -> None:
        """Processes AI logic for all entities.

        Args:
            game_state: The current state of the game.
        """
        for entity_id, components in game_state.entities.items():
            player = components.get(Player)
            if not player:
                continue

            # Neutral units (Player 0) are passive and do not auto-acquire targets.
            if player.player_id == 0:
                continue

            attack = components.get(Attack)
            if not attack:
                continue

            # Find a target if we don't have one
            # Auto-targeting enabled for FFA behavior.
            if not attack.attack_target:
                vision = components.get(Vision)
                if vision:
                    my_pos = components.get(Position)
                    if my_pos:
                        closest_enemy = Targeting.find_closest_enemy(entity_id, my_pos, player, vision, game_state)
                        if closest_enemy:
                            log.debug(
                                f"Entity {entity_id} (Player {player.player_id}) "
                                f"acquired target {closest_enemy} at {my_pos}"
                            )
                            attack.attack_target = closest_enemy
