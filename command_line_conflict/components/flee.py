from .base import Component


class Flee(Component):
    """Enables an entity to flee from perceived threats.

    This component can trigger fleeing behavior based on a health threshold or
    the presence of enemies.

    Attributes:
        flee_health_threshold (float | None): The health percentage below which
            the entity will attempt to flee. If None, health is not a trigger.
        flees_from_enemies (bool): If True, the entity will flee when enemies
            are detected, regardless of health.
        is_fleeing (bool): A flag indicating whether the entity is currently
            in a fleeing state.
    """

    def __init__(
        self, flee_health_threshold: float | None = None, flees_from_enemies=False
    ):
        """Initializes the Flee component.

        Args:
            flee_health_threshold: The health percentage at which the entity will
                                 start fleeing.
            flees_from_enemies: Whether the entity flees from enemies.
        """
        self.flee_health_threshold = flee_health_threshold
        self.flees_from_enemies = flees_from_enemies
        self.is_fleeing = False
