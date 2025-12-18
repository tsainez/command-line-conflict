from .. import config
from ..components.attack import Attack
from ..components.health import Health
from ..components.movable import Movable
from ..components.player import Player  # TODO: Remove unused import.
from ..components.position import Position
from ..components.unit_identity import UnitIdentity
from ..components.vision import Vision  # TODO: Remove unused import.
from ..factories import create_confetti
from ..game_state import GameState
from ..logger import log


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
        for entity_id, components in list(game_state.entities.items()):
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
                            # Get entity names for logging
                            attacker_identity = components.get(UnitIdentity)
                            attacker_name = (
                                attacker_identity.name
                                if attacker_identity
                                else f"Entity {entity_id}"
                            )

                            target_identity = target_components.get(UnitIdentity)
                            target_name = (
                                target_identity.name
                                if target_identity
                                else f"Entity {attack.attack_target}"
                            )

                            log.info(
                                f"{attacker_name} attacks {target_name} "
                                f"for {attack.attack_damage} damage."
                            )
                        target_health.hp -= attack.attack_damage

                        # Trigger attack sound
                        game_state.add_event(
                            {
                                "type": "sound",
                                "data": {
                                    "name": (
                                        "attack_melee"
                                        if attack.attack_range <= 1.5
                                        else "attack_ranged"
                                    )
                                },
                            }
                        )
                        # Retaliation Logic:
                        # If the target has an Attack component and no current target, make them fight back.
                        target_attack = target_components.get(Attack)
                        if target_attack and target_attack.attack_target is None:
                            target_attack.attack_target = entity_id

                        if attack.attack_range > 1:
                            create_confetti(game_state, target_pos.x, target_pos.y)
                            if config.DEBUG:
                                log.info(
                                    f"Confetti effect created at ({target_pos.x}, {target_pos.y})"
                                )
                        attack.attack_cooldown = 1 / attack.attack_speed
                else:
                    # Move towards target
                    movable = components.get(Movable)
                    if movable and not movable.hold_position:
                        movable.target_x = target_pos.x
                        movable.target_y = target_pos.y
