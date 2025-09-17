from .. import config
from ..logger import log
from ..game_state import GameState
from ..components.position import Position
from ..components.attack import Attack
from ..components.health import Health
from ..components.vision import Vision
from ..components.movable import Movable
from ..components.player import Player


class CombatSystem:
    """Handles combat interactions between entities."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes combat logic for all entities.
        This method iterates through all entities with an Attack component,
        manages attack cooldowns, finds targets, and executes attacks.
        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in game_state.entities.items():
            attack = components.get(Attack)
            if not attack:
                continue

            # Cooldowns
            if attack.attack_cooldown > 0:
                attack.attack_cooldown -= dt

            # Attack the target if we have one
            if attack.attack_target:
                target_components = game_state.entities.get(attack.attack_target)
                if not target_components:
                    attack.attack_target = None
                    continue

                target_health = target_components.get(Health)
                if not target_health or target_health.hp <= 0:
                    attack.attack_target = None
                    continue

                my_pos = components.get(Position)
                target_pos = target_components.get(Position)
                if not my_pos or not target_pos:
                    continue

                dist_to_target = (
                    (my_pos.x - target_pos.x) ** 2 + (my_pos.y - target_pos.y) ** 2
                ) ** 0.5

                if dist_to_target <= attack.attack_range:
                    # Stop moving and attack
                    movable = components.get(Movable)
                    if movable:
                        movable.path = []
                        movable.target_x, movable.target_y = my_pos.x, my_pos.y

                    if attack.attack_cooldown <= 0 and attack.attack_damage > 0:
                        if config.DEBUG:
                            log.info(
                                f"Entity {entity_id} attacks {attack.attack_target} "
                                f"for {attack.attack_damage} damage."
                            )
                        target_health.hp -= attack.attack_damage
                        attack.attack_cooldown = 1 / attack.attack_speed
                else:
                    # Move towards target
                    movable = components.get(Movable)
                    if movable:
                        movable.target_x = target_pos.x
                        movable.target_y = target_pos.y

