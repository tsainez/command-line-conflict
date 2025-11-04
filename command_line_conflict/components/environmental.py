from dataclasses import dataclass

@dataclass
class Environmental:
    """A component that stores the environmental settings for the map."""
    is_day: bool = True
    fog_of_war: bool = False
