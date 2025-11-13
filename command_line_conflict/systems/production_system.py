from ..components.production import Production
from ..components.position import Position
from .. import factories

class ProductionSystem:
    """A system that handles the logic of producing units."""

    def update(self, game_state, dt):
        """Updates the production state of all buildings.
        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in game_state.entities.items():
            production = components.get(Production)
            if production and production.queue:
                production.progress += dt
                if production.progress >= production.time_to_produce:
                    unit_type = production.queue.pop(0)
                    position = components.get(Position)
                    if unit_type == "chassis":
                        factories.create_chassis(game_state, position.x + 2, position.y + 2, components.get("Player").player_id, components.get("Player").is_human)
                    production.progress = 0.0
