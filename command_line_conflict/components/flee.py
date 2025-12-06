from .base import Component


class Flee(Component):
    """A component that gives an entity the ability to flee."""

    def __init__(
        self, flee_health_threshold: float | None = None, flees_from_enemies=False
    ) -> None:
        """Initializes the Flee component.

        Args:
            flee_health_threshold: The health percentage at which the entity will
                                 start fleeing.
            flees_from_enemies: Whether the entity flees from enemies.
        """
        self.flee_health_threshold = flee_health_threshold
        self.flees_from_enemies = flees_from_enemies
        self.is_fleeing = False
