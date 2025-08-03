from .base import Unit


class Chassis(Unit):
    """
    A basic, cheap, melee combat unit. It can attack enemies in adjacent cells, and pathfind to reach them.
    It's affordability makes it easy to produce in large numbers, but it is weak to being kited by ranged units.
    """

    icon = "C"
    max_hp = 80
    attack_damage = 10
    attack_range = 1
    speed = 2
