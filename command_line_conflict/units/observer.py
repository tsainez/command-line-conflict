from .base import Unit


class Observer(Unit):
    """
    A fast, non-combat unit with a large vision range. It will flee from
    enemies.
    """

    icon = "O"
    max_hp = 40
    attack_damage = 0
    attack_range = 0
    speed = 4
    vision_range = 15
    flees_from_enemies = True
