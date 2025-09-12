from ..game_state import GameState
from ..components.health import Health
from ..components.dead import Dead
from ..components.movable import Movable
from ..components.attack import Attack
from ..components.selectable import Selectable
from ..components.flee import Flee


class HealthSystem:
    """
    This system is responsible for handling health regeneration and unit death.
    """

    def update(self, game_state: GameState, dt: float) -> None:
        for entity_id, components in list(game_state.entities.items()):
            health = components.get(Health)

            if not health:
                continue

            if health.hp <= 0:
                if not components.get(Dead):
                    game_state.add_component(entity_id, Dead())
                    game_state.remove_component(entity_id, Movable)
                    game_state.remove_component(entity_id, Attack)
                    game_state.remove_component(entity_id, Selectable)
                    game_state.remove_component(entity_id, Flee)
            elif health.hp < health.max_hp:
                health.hp += health.health_regen_rate * dt
                health.hp = min(health.hp, health.max_hp)
