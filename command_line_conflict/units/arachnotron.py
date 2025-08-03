from .base import Unit


class Arachnotron(Unit):
    """
    A specialized ranged unit designed to break stalemates and static defenses. 
    This unit can bypass obstacles and attack from a distance, making it effective against fortified positions.
    """

    icon = "A"
    max_hp = 120
    attack_damage = 20
    attack_range = 6
    speed = 1.8
    can_fly = True
