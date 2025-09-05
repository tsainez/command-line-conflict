from .base import Component


class Flee(Component):
    """
    A component that gives an entity the ability to flee.
    """

    def __init__(
        self, flee_health_threshold: float | None = None, flees_from_enemies=False
    ):
        self.flee_health_threshold = flee_health_threshold
        self.flees_from_enemies = flees_from_enemies
        self.is_fleeing = False
