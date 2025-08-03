from .base import Unit


class Arachnotron(Unit):
    """
    A flying unit that can move over any terrain.
    """

    icon = "A"
    max_hp = 120
    attack_damage = 20
    attack_range = 6
    speed = 1.8
    can_fly = True
