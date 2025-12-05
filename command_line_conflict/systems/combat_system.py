from .. import config
from ..components.attack import Attack
from ..components.health import Health
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..factories import create_confetti
from ..game_state import GameState
from ..logger import log
from ..systems.movement_system import MovementSystem
from ..utils.targeting import Targeting


class CombatSystem:
    """Handles combat interactions between entities."""

    def __init__(self):
        self.movement_system = MovementSystem()

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

            # Validate current target
            if attack.attack_target:
                target_components = game_state.entities.get(attack.attack_target)
                if not target_components:
                    attack.attack_target = None
                else:
                    target_health = target_components.get(Health)
                    if not target_health or target_health.hp <= 0:
                        attack.attack_target = None

            # Auto-acquire target if needed
            if not attack.attack_target:
                movable = components.get(Movable)
                # Check if we should scan for targets
                # Scan if:
                # 1. Idle (no path) - Auto-attack (Standard RTS behavior)
                # 2. Attack Moving (path exists AND attack_move_target is set)
                should_scan = False
                if movable:
                    if not movable.path:
                        should_scan = True
                    elif movable.attack_move_target:
                        should_scan = True
                else:
                    # Immobile units (turrets) always scan
                    should_scan = True

                if should_scan:
                    vision = components.get(Vision)
                    player = components.get(Player)
                    my_pos = components.get(Position)
                    if vision and player and my_pos:
                        closest_enemy = Targeting.find_closest_enemy(
                            entity_id, my_pos, player, vision, game_state
                        )
                        if closest_enemy:
                            attack.attack_target = closest_enemy
                            if movable:
                                movable.path = []
                                movable.target_x, movable.target_y = my_pos.x, my_pos.y

            # Resume Attack Move if idle and have a pending target
            if not attack.attack_target:
                movable = components.get(Movable)
                if (
                    movable
                    and movable.attack_move_target
                    and not movable.path
                ):
                    # We have an attack move target, but no path (stopped).
                    # Check if we are at the target
                    curr_pos = components.get(Position)
                    tx, ty = movable.attack_move_target
                    if curr_pos:
                        dx = curr_pos.x - tx
                        dy = curr_pos.y - ty
                        if (dx * dx + dy * dy) > 0.01:
                            # Not at target, resume movement
                            # We use the pre-instantiated MovementSystem.
                            self.movement_system.set_target(
                                game_state, entity_id, tx, ty, is_attack_move=True
                            )

            # Attack the target if we have one
            if attack.attack_target:
                target_components = game_state.entities.get(attack.attack_target)
                # Validation already done above, but we need target_health
                if not target_components:
                    continue
                target_health = target_components.get(Health)

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
                            log.info(  # TODO: Can we get the entity names here?
                                f"Entity {entity_id} attacks {attack.attack_target} "
                                f"for {attack.attack_damage} damage."
                            )
                        target_health.hp -= attack.attack_damage
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
                    if movable:
                        movable.target_x = target_pos.x
                        movable.target_y = target_pos.y
