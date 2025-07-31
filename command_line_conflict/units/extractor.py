from .base import Unit


class Extractor(Unit):
    """
    A unit that can harvest resources but has no combat capabilities.
    """

    icon = "E"
    max_hp = 50
    attack_damage = 0
    attack_range = 0
    speed = 1.5
