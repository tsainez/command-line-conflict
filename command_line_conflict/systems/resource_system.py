from ..components.dead import Dead
from ..components.player import Player
from ..components.position import Position
from ..components.resource_deposit import ResourceDeposit
from ..game_state import GameState
from ..logger import log


class ResourceSystem:
    """System that handles resource collection/harvesting from scrap entities."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Checks for player units overlapping with scrap deposits and harvests them.

        Args:
            game_state: The current state of the game.
            dt: Delta time (unused but required by interface).
        """
        # Find all entities with ResourceDeposit component
        scrap_entities = list(game_state.get_entities_with_component(ResourceDeposit))

        for scrap_id in scrap_entities:
            components = game_state.entities.get(scrap_id)
            if not components:
                continue

            deposit = components.get(ResourceDeposit)
            pos = components.get(Position)
            if not deposit or not pos:
                continue

            # Find who is at this integer position
            cell_entities = game_state.get_entities_at_position(int(pos.x), int(pos.y))
            for ent_id in cell_entities:
                if ent_id == scrap_id:
                    continue

                # Must not be dead
                if game_state.get_component(ent_id, Dead):
                    continue

                player = game_state.get_component(ent_id, Player)
                # Player units only, excluding neutral (player_id = 0)
                if player and player.player_id != 0:
                    player_id = player.player_id
                    current_resources = game_state.resources.get(player_id, 0)
                    game_state.resources[player_id] = current_resources + deposit.amount

                    log.info(
                        f"Player {player_id} harvested {deposit.amount} resources from scrap {scrap_id} "
                        f"(New total: {game_state.resources[player_id]})"
                    )

                    # Trigger visual floating text event
                    game_state.add_event(
                        {
                            "type": "visual_effect",
                            "subtype": "floating_text",
                            "x": pos.x,
                            "y": pos.y,
                            "text": f"+{deposit.amount} Scrap",
                            "color": (255, 215, 0),  # Gold color
                        }
                    )

                    # Trigger sound event
                    game_state.add_event({"type": "sound", "data": {"name": "spawn_unit"}})

                    # Remove the scrap entity from the game
                    game_state.remove_entity(scrap_id)
                    break  # Consumed this scrap pile
