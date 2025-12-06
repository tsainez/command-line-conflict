"""This module contains the UnitIdentity component."""

from .base import Component


class UnitIdentity(Component):
    """Component that identifies a unit's type (e.g., 'chassis', 'rover')."""

    def __init__(self, name: str) -> None:
        """Initializes the UnitIdentity component.

        Args:
            name: The name of the unit type.
        """
        self.name = name
