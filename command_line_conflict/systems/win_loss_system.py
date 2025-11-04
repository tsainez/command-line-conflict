from ..components.building import Building
from ..components.player import Player


class WinLossSystem:
    """A system that checks for win/loss conditions."""

    def update(self, game_state):
        """Checks if either player has lost all their buildings.
        Args:
            game_state: The current state of the game.
        """
        player_buildings = {1: 0, 2: 0}
        for entity_id, components in game_state.entities.items():
            if Building in components:
                player = components.get(Player)
                if player:
                    player_buildings[player.player_id] += 1

        if player_buildings[1] == 0:
            game_state.winner = 2
        elif player_buildings[2] == 0:
            game_state.winner = 1
