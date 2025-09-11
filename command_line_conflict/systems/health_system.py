from ..game_state import GameState
from ..components.health import Health


class HealthSystem:
    """
    This system is responsible for handling health regeneration.
    """

    def update(self, game_state: GameState, dt: float) -> None:
        for entity_id, components in game_state.entities.items():
            health = components.get(Health)

            if health:
                if health.hp < health.max_hp:
                    health.hp += health.health_regen_rate * dt
                    health.hp = min(health.hp, health.max_hp)
