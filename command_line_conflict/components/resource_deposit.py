from .base import Component


class ResourceDeposit(Component):
    """A component that marks an entity as containing harvestable resources."""

    def __init__(self, amount: int = 50):
        """Initializes the ResourceDeposit component.

        Args:
            amount: The amount of resources in this deposit.
        """
        self.amount = amount
