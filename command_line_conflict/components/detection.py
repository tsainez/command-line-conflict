from .base import Component


class Detection(Component):
    """Gives an entity the ability to detect other entities within a certain range.

    Attributes:
        detection_range (int): The maximum distance at which this entity can
            detect other entities.
    """

    def __init__(self, detection_range: int):
        """Initializes the Detection component.

        Args:
            detection_range: The maximum distance from which the entity can detect.
        """
        self.detection_range = detection_range
