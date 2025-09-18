from .. import config
from ..components.attack import Attack
from ..components.dead import Dead
from ..components.flee import Flee
from ..components.health import Health
from ..components.movable import Movable
from ..components.selectable import Selectable
from ..game_state import GameState
from ..logger import \
    log  # TODO: Expand logger usage, specifically for when in debug mode. Can we log more than just deaths?


class HealthSystem:
    """Manages entity health, including regeneration and death."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes health regeneration and handles entity death.

        This method iterates through all entities with a Health component.
        It applies health regeneration and marks entities with zero or less
        health as Dead, removing other components to prevent further actions.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            health = components.get(Health)

            if not health:
                continue

            if health.hp <= 0:
                if not components.get(Dead):
                    if config.DEBUG:
                        log.info(f"Entity {entity_id} has died.")
                    game_state.add_component(entity_id, Dead())
                    game_state.remove_component(entity_id, Movable)
                    game_state.remove_component(entity_id, Attack)
                    game_state.remove_component(entity_id, Selectable)
                    game_state.remove_component(entity_id, Flee)
            elif health.hp < health.max_hp:
                health.hp += health.health_regen_rate * dt
                health.hp = min(health.hp, health.max_hp)
