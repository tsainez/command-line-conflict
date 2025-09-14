from command_line_conflict.game_state import GameState
from command_line_conflict.components.production import Production
from command_line_conflict.components.position import Position
from command_line_conflict.components.player import Player
from command_line_conflict import factories

class ProductionSystem:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.unit_build_times = {
            "chassis": 5,
            "rover": 7,
            "arachnotron": 10,
            "observer": 8,
            "immortal": 12,
            "extractor": 6,
        }

    def update(self, dt: float) -> None:
        for entity_id, components in self.game_state.entities.items():
            production = components.get(Production)
            if not production or not production.production_queue:
                continue

            unit_to_build = production.production_queue[0]
            build_time = self.unit_build_times.get(unit_to_build, 5)

            production.progress += dt
            if production.progress >= build_time:
                production.progress = 0
                production.production_queue.pop(0)

                position = components.get(Position)
                player = components.get(Player)

                if position and player:
                    # Spawn the new unit next to the factory
                    new_unit_x = position.x + 1
                    new_unit_y = position.y

                    factory_function = getattr(factories, f"create_{unit_to_build}", None)
                    if factory_function:
                        factory_function(self.game_state, new_unit_x, new_unit_y, player.player_id)
