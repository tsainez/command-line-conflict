from .base import Component

class Factory(Component):
    """A component that allows an entity to produce other units."""
    def __init__(self, unit_types: list[str], production_time: float):
        self.unit_types = unit_types
        self.production_time = production_time
        self.production_queue: list[str] = []
        self.production_progress = 0.0