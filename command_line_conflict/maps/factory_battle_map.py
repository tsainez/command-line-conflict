from __future__ import annotations

from typing import TYPE_CHECKING

from .. import factories
from .base import Map

if TYPE_CHECKING:
    from ..game_state import GameState


class FactoryBattleMap(Map):
    """A map with enemy factories and defenders for the player to fight against."""

    def __init__(self, width: int = 60, height: int = 40) -> None:
        """Initializes the FactoryBattleMap.

        Args:
            width: The width of the map.
            height: The height of the map.
        """
        super().__init__(width, height)
        self._create_walls()

    def _create_walls(self) -> None:
        """Creates the walls for the map."""
        # Create a central arena with some cover
        # Vertical barriers
        for y in range(10, 30):
            self.add_wall(20, y)
            self.add_wall(40, y)

        # Horizontal barriers to create chokepoints
        for x in range(20, 25):
            self.add_wall(x, 10)
            self.add_wall(x, 30)

        for x in range(35, 40):
            self.add_wall(x, 10)
            self.add_wall(x, 30)

        # Some scattered cover
        for i in range(5):
            self.add_wall(10 + i, 20)
            self.add_wall(45 + i, 20)

    def create_initial_units(self, game_state: "GameState") -> None:
        """Creates the initial units for the map.

        Args:
            game_state: The game state to add units to.
        """
        # Player 1 units (Human) - Start at the top left area
        for i in range(3):
            factories.create_chassis(game_state, 5 + i * 2, 5, player_id=1, is_human=True)

        factories.create_rover(game_state, 8, 8, player_id=1, is_human=True)

        # Player 2 units (AI) - Enemy Base at bottom right

        # Factories
        factories.create_rover_factory(game_state, 50, 30, player_id=2, is_human=False)
        factories.create_arachnotron_factory(game_state, 55, 35, player_id=2, is_human=False)

        # Defenders
        factories.create_rover(game_state, 48, 28, player_id=2, is_human=False)
        factories.create_rover(game_state, 52, 32, player_id=2, is_human=False)
        factories.create_arachnotron(game_state, 54, 34, player_id=2, is_human=False)

        # Some wildlife in the middle
        factories.create_wildlife(game_state, 30, 20)
        factories.create_wildlife(game_state, 32, 22)
