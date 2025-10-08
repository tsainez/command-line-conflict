from .base import Component

class Builder(Component):
    """A component that allows an entity to build structures."""
    def __init__(self, build_types: list[str]):
        self.build_types = build_types
        self.build_target: int | None = None
        self.build_progress = 0.0