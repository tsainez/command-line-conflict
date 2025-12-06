from .base import Component


class Confetti(Component):
    """A component that represents a confetti effect."""

    def __init__(self, lifetime: float) -> None:
        """Initializes the Confetti component.

        Args:
            lifetime: The duration of the confetti effect in seconds.
        """
        self.lifetime = lifetime
