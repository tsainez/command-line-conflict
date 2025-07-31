from .base import Unit


class Rover(Unit):
    """
    A ranged combat unit that cannot pathfind around obstacles.
    """

    icon = "R"
    max_hp = 60
    attack_damage = 15
    attack_range = 5
    speed = 2.5

    def set_target(self, x: int, y: int, game_map=None) -> None:
        """
        Set the target for the Rover. It moves in a straight line and does not
        use pathfinding.
        """
        self.order_target = (x, y)
        self.target_x = x
        self.target_y = y
        self.path = []
