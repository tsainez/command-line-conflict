from .base import Component


class Detection(Component):
    """
    A component that gives an entity a detection range.
    """

    def __init__(self, detection_range: int):
        """Initializes the Detection component.

        Args:
            detection_range: The maximum distance from which the entity can detect.
        """
        self.detection_range = detection_range
