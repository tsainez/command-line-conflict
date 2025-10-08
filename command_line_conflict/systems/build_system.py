from ..components.builder import Builder
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..factories import create_unit_factory
from ..game_state import GameState


class BuildSystem:
    """Handles the construction of buildings by builder units."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Processes the construction logic for all builder units.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            builder = components.get(Builder)
            if not builder or not builder.build_target:
                continue

            target_entity = game_state.entities.get(builder.build_target)
            if not target_entity:
                builder.build_target = None
                continue

            my_pos = components.get(Position)
            target_pos = target_entity.get(Position)

            dist_sq = (my_pos.x - target_pos.x) ** 2 + (my_pos.y - target_pos.y) ** 2

            if dist_sq <= 2**2:  # Build range of 2
                movable = components.get(Movable)
                if movable:
                    movable.path = []
                    movable.target_x, movable.target_y = my_pos.x, my_pos.y

                builder.build_progress += dt
                if builder.build_progress >= 5.0:  # 5 seconds to build
                    player = components.get(Player)
                    create_unit_factory(
                        game_state,
                        target_pos.x,
                        target_pos.y,
                        player.player_id,
                        player.is_human,
                    )
                    game_state.remove_entity(builder.build_target)
                    builder.build_target = None
                    builder.build_progress = 0.0