from .base import Map
from .. import factories


class FactoryMap(Map):
    """A map featuring enemy factories for the player to fight against."""

    def __init__(self) -> None:
        """Initializes the FactoryMap."""
        super().__init__(width=50, height=40)

        # Create a base perimeter for the enemy (Player 2)
        # Top wall of the base
        for x in range(30, 48):
            self.add_wall(x, 25)
        # Left wall of the base
        for y in range(25, 38):
            self.add_wall(30, y)

        # Some random obstacles in the middle
        self.add_wall(20, 20)
        self.add_wall(21, 20)
        self.add_wall(20, 21)
        self.add_wall(25, 15)
        self.add_wall(25, 16)
        self.add_wall(25, 17)

    def initialize_entities(self, game_state) -> None:
        """Initializes the map with factories and units."""

        # Player 1 (Human) starts at top-left
        for i in range(3):
            factories.create_chassis(
                game_state, 5 + i * 2, 5, player_id=1, is_human=True
            )

        # Give Player 1 a bit more firepower to start with against factories
        factories.create_rover(
            game_state, 8, 8, player_id=1, is_human=True
        )

        # Player 2 (AI) Base at bottom-right

        # Factories
        factories.create_rover_factory(
            game_state, 40, 30, player_id=2, is_human=False
        )
        factories.create_arachnotron_factory(
            game_state, 35, 35, player_id=2, is_human=False
        )

        # Defenders
        for i in range(3):
            factories.create_rover(
                game_state, 35 + i * 2, 28, player_id=2, is_human=False
            )

        # Some initial wildlife
        factories.create_wildlife(game_state, 20, 25)
        factories.create_wildlife(game_state, 25, 10)
