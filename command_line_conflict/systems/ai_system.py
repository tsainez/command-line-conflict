from ..components.attack import Attack
from ..components.player import Player
from ..components.position import Position
from ..components.renderable import Renderable
from ..components.vision import Vision
from ..game_state import GameState
from ..utils.targeting import Targeting

# TODO: Integrate logger for debug mode. Currently not used.


class AISystem:
    """Controls the behavior of AI-controlled entities."""

    def update(self, game_state: GameState) -> None:
        """Processes AI logic for all entities.

        Args:
            game_state: The current state of the game.
        """
        for entity_id, components in list(game_state.entities.items()):
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
                        # 1. Prioritize finding and attacking enemies
                        closest_enemy = Targeting.find_closest_enemy(
                            entity_id, my_pos, player, vision, game_state
                        )
                        if closest_enemy:
                            attack.attack_target = closest_enemy
                            continue

                        # 2. If no enemies, and I am an extractor, find minerals
                        renderable = components.get(Renderable)
                        if renderable and renderable.icon == "E":
                            closest_minerals = Targeting.find_closest_minerals(
                                entity_id, my_pos, vision, game_state
                            )
                            if closest_minerals:
                                attack.attack_target = closest_minerals