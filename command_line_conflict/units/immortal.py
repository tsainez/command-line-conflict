from .base import Unit


class Immortal(Unit):
    """
    A powerful ranged unit with health regeneration. 
    It will automatically flee when its health is low.
    While other units will self-sacrifice, this unit survives to fight another day.
    """

    icon = "I"
    max_hp = 150
    attack_damage = 25
    attack_range = 7
    speed = 2
    health_regen_rate = 2.0
    flee_health_threshold = 0.2  # Flee at 20% health
