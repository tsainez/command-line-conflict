from .base import Unit


class Observer(Unit):
    """
    An unarmed scouting unit dedicated for intelligence gathering. It has a large vision range, and can traverse over obstacles. 
    It will intentionally avoid combat by detecting enemies from a distance, and navigating around their detection range
    """

    icon = "O"
    max_hp = 40
    attack_damage = 0
    attack_range = 0
    speed = 4
    vision_range = 15
    flees_from_enemies = True
