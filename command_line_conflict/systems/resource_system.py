from ..components.gatherer import Gatherer
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.resource import Resource
from ..game_state import GameState


class ResourceSystem:
    """Handles the resource gathering process for gatherer units."""

    def update(self, game_state: GameState, dt: float) -> None:
        """
        Processes the resource gathering logic for all gatherer units.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            gatherer = components.get(Gatherer)
            if not gatherer or not gatherer.target_resource_id:
                continue

            my_pos = components.get(Position)
            target_entity = game_state.entities.get(gatherer.target_resource_id)
            if not target_entity:
                gatherer.target_resource_id = None
                continue

            target_pos = target_entity.get(Position)
            dist_sq = (my_pos.x - target_pos.x) ** 2 + (my_pos.y - target_pos.y) ** 2

            if dist_sq <= 2**2:  # Gather range of 2
                movable = components.get(Movable)
                if movable:
                    movable.path = []

                gatherer.is_gathering = True
                gatherer.gather_cooldown -= dt
                if gatherer.gather_cooldown <= 0:
                    resource = target_entity.get(Resource)
                    if resource and resource.amount > 0:
                        amount_to_gather = gatherer.gather_rate
                        actual_gathered = min(amount_to_gather, resource.amount, gatherer.capacity - gatherer.amount_carried)

                        gatherer.amount_carried += actual_gathered
                        resource.amount -= actual_gathered

                        player = components.get(Player)
                        if player:
                            game_state.resources[player.player_id][resource.resource_type] += actual_gathered

                        gatherer.gather_cooldown = 1.0  # 1 second per gather action
            else:
                movable = components.get(Movable)
                if movable and not movable.path:
                    game_state.map.find_path(
                        (int(my_pos.x), int(my_pos.y)),
                        (int(target_pos.x), int(target_pos.y)),
                    )