from ..components.attack import Attack
from ..components.flee import Flee
from ..components.health import Health
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..game_state import GameState
from ..utils.targeting import Targeting

# TODO: Integrate logger for debug mode. Currently not used.


class FleeSystem:
    """Handles the logic for entities fleeing from enemies.

    This system checks for conditions that would cause an entity to flee,
    such as low health or the presence of enemies. When an entity is fleeing,
    it will move away from the nearest threat.
    """

    def __init__(self):
        pass

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes the fleeing logic for all entities.

        This method checks for conditions that would cause an entity to flee,
        such as low health or the presence of enemies, and then sets a
        fleeing destination for the entity.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in game_state.entities.items():
            flee = components.get(Flee)
            if not flee:
                continue

            health = components.get(Health)
            vision = components.get(Vision)
            my_pos = components.get(Position)
            my_player = components.get(Player)

            if not health or not vision or not my_pos or not my_player:
                continue

            is_low_health = (
                flee.flee_health_threshold is not None
                and health.hp / health.max_hp <= flee.flee_health_threshold
            )
            closest_enemy = Targeting.find_closest_enemy(
                entity_id, my_pos, my_player, vision, game_state
            )
            sees_enemy = closest_enemy is not None

            if not flee.is_fleeing:
                if (is_low_health or flee.flees_from_enemies) and sees_enemy:
                    flee.is_fleeing = True
                    attack = components.get(Attack)
                    if attack:
                        attack.attack_target = None
            else:  # is fleeing
                if not sees_enemy and not is_low_health:
                    flee.is_fleeing = False

            if flee.is_fleeing:
                attack = components.get(Attack)
                if attack:
                    attack.attack_target = None

                if closest_enemy:
                    enemy_components = game_state.entities.get(closest_enemy)
                    if enemy_components:
                        enemy_pos = enemy_components.get(Position)
                        if enemy_pos:
                            dx = my_pos.x - enemy_pos.x
                            dy = my_pos.y - enemy_pos.y
                            dist = (dx**2 + dy**2) ** 0.5
                            if dist > 0:
                                flee_x = my_pos.x + dx / dist * 5
                                flee_y = my_pos.y + dy / dist * 5
                                movable = components.get(Movable)
                                if movable:
                                    movable.target_x = flee_x
                                    movable.target_y = flee_y
