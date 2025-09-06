from ..game_state import GameState
from ..components.health import Health


class HealthSystem:
    """
    This system is responsible for handling health, regeneration, and death.
    """

    def update(self, game_state: GameState, dt: float) -> None:
        dead_entities = []
        for entity_id, components in game_state.entities.items():
            health = components.get(Health)

            if not health:
                continue

            # Handle death
            if health.hp <= 0:
                dead_entities.append(entity_id)
                continue

            # Handle regeneration
            if health.hp < health.max_hp:
                health.hp += health.health_regen_rate * dt
                health.hp = min(health.hp, health.max_hp)

        # Remove dead entities
        for entity_id in dead_entities:
            del game_state.entities[entity_id]
            if game_state.sound_system:
                game_state.sound_system.play_sound("explosion")
