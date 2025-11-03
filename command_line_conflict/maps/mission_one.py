from .base import Map

class MissionOne(Map):
    """The first mission of the campaign."""

    def __init__(self) -> None:
        """Initializes the MissionOne map."""
        super().__init__(width=30, height=20)

        # Add some mineral patches
        self.add_mineral_patch(5, 5)
        self.add_mineral_patch(5, 6)
        self.add_mineral_patch(6, 5)
        self.add_mineral_patch(6, 6)

        self.add_mineral_patch(23, 13)
        self.add_mineral_patch(23, 14)
        self.add_mineral_patch(24, 13)
        self.add_mineral_patch(24, 14)


        # Add a pre-placed enemy unit
        # self.add_unit(20, 10, "enemy_chassis", 2)
