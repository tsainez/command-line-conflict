from .base import Component

class Resource(Component):
    """A component for entities that can be harvested for resources."""
    def __init__(self, resource_type: str = "minerals", amount: int = 10000):
        self.resource_type = resource_type
        self.amount = amount