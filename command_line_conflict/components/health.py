from .base import Component


class Health(Component):
    """A component that gives an entity health."""

    def __init__(self, hp: int, max_hp: int, health_regen_rate: float = 0.0) -> None:
        """Initializes the Health component.

        Args:
            hp: The current health of the entity.
            max_hp: The maximum health of the entity.
            health_regen_rate: The rate at which the entity regenerates health.
        """
        self.hp = hp
        self.max_hp = max_hp
        self.health_regen_rate = health_regen_rate
