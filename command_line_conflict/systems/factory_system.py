from ..components.factory import Factory
from ..components.player import Player
from ..components.position import Position
from ..factories import create_chassis, create_extractor
from ..game_state import GameState


class FactorySystem:
    """Handles unit production from factory buildings."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes the unit production logic for all factories.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            factory = components.get(Factory)
            if not factory or not factory.production_queue:
                continue

            factory.production_progress += dt
            if factory.production_progress >= factory.production_time:
                unit_type = factory.production_queue.pop(0)
                player = components.get(Player)
                position = components.get(Position)
                spawn_x, spawn_y = position.x, position.y + 2  # Spawn below factory

                if unit_type == "chassis":
                    create_chassis(
                        game_state,
                        spawn_x,
                        spawn_y,
                        player.player_id,
                        player.is_human,
                    )
                elif unit_type == "extractor":
                    create_extractor(
                        game_state,
                        spawn_x,
                        spawn_y,
                        player.player_id,
                        player.is_human,
                    )

                factory.production_progress = 0.0