from .base import Component


class Health(Component):
    """Manages an entity's health points, including regeneration.

    Attributes:
        hp (int): The current health points of the entity.
        max_hp (int): The maximum health points the entity can have.
        health_regen_rate (float): The amount of health regenerated per second.
            A value of 0.0 means no regeneration.
    """

    def __init__(self, hp: int, max_hp: int, health_regen_rate: float = 0.0):
        """Initializes the Health component.

        Args:
            hp: The current health of the entity.
            max_hp: The maximum health of the entity.
            health_regen_rate: The rate at which the entity regenerates health.
        """
        self.hp = hp
        self.max_hp = max_hp
        self.health_regen_rate = health_regen_rate
