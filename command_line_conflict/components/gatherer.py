from .base import Component

class Gatherer(Component):
    """
    A component that gives an entity the ability to gather resources.
    """
    def __init__(self, gather_rate: float = 5.0, capacity: int = 10):
        """
        Initializes the Gatherer component.

        Args:
            gather_rate: The amount of resources gathered per second.
            capacity: The maximum amount of resources the unit can carry.
        """
        self.gather_rate = gather_rate
        self.capacity = capacity
        self.target_resource_id: int | None = None
        self.is_gathering = False
        self.is_returning = False
        self.amount_carried = 0
        self.gather_cooldown = 0.0