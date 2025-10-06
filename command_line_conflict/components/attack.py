from .base import Component


class Attack(Component):
    """Gives an entity the ability to attack other entities.

    Attributes:
        attack_damage (int): The amount of damage the entity inflicts per attack.
        attack_range (int): The maximum distance from which the entity can attack.
        attack_speed (float): The time in seconds between consecutive attacks.
        attack_target (int | None): The ID of the entity currently being targeted.
        attack_cooldown (float): The time remaining until the entity can attack again.
    """

    def __init__(self, attack_damage: int, attack_range: int, attack_speed: float):
        """Initializes the Attack component.

        Args:
            attack_damage: The amount of damage the entity can inflict.
            attack_range: The maximum distance from which the entity can attack.
            attack_speed: The time in seconds between attacks.
        """
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.attack_speed = attack_speed
        self.attack_target: int | None = None
        self.attack_cooldown = 0.0
