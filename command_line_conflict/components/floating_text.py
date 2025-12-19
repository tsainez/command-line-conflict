from .base import Component


class FloatingText(Component):
    """A component for floating text effects (e.g. damage numbers)."""

    def __init__(
        self,
        text: str,
        color: tuple[int, int, int],
        lifetime: float,
        speed: float = 2.0,
    ):
        """Initializes the FloatingText component.

        Args:
            text: The text to display.
            color: The color of the text (R, G, B).
            lifetime: How long the text remains visible in seconds.
            speed: Vertical speed in grid cells per second.
        """
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.speed = speed
