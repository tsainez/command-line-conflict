from .base import Component


class Attack(Component):
    """
    A component that gives an entity the ability to attack.
    """

    def __init__(self, attack_damage: int, attack_range: int, attack_speed: float):
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.attack_speed = attack_speed
        self.attack_target: int | None = None
        self.attack_cooldown = 0.0
