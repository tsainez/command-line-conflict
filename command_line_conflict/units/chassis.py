from .base import Unit


class Chassis(Unit):
    """
    A basic, cheap, melee combat unit.
    """

    icon = "C"
    max_hp = 80
    attack_damage = 10
    attack_range = 1
    speed = 2
