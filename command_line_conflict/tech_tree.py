from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class TechNode:
    """Represents a node in the tech tree."""
    id: str
    name: str
    description: str
    type: str  # "unit", "upgrade"
    cost: int = 0
    # Modifiers: e.g., {"unit_id": "rover", "stat": "hp", "value": 10, "operation": "add"}
    modifiers: List[Dict] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    mutually_exclusive_with: List[str] = field(default_factory=list)

# Define the Tech Tree
TECH_TREE: Dict[str, TechNode] = {
    # Units
    "unlock_rover": TechNode(
        id="unlock_rover",
        name="Unlock Rover",
        description="Unlocks the Rover unit.",
        type="unit",
        modifiers=[{"unit_id": "rover", "stat": "unlock", "value": True}]
    ),
    "unlock_arachnotron": TechNode(
        id="unlock_arachnotron",
        name="Unlock Arachnotron",
        description="Unlocks the Arachnotron unit.",
        type="unit",
        prerequisites=["unlock_rover"],
        modifiers=[{"unit_id": "arachnotron", "stat": "unlock", "value": True}]
    ),
    "unlock_observer": TechNode(
        id="unlock_observer",
        name="Unlock Observer",
        description="Unlocks the Observer unit.",
        type="unit",
        prerequisites=["unlock_rover"],
        modifiers=[{"unit_id": "observer", "stat": "unlock", "value": True}]
    ),
     "unlock_immortal": TechNode(
        id="unlock_immortal",
        name="Unlock Immortal",
        description="Unlocks the Immortal unit.",
        type="unit",
        prerequisites=["unlock_arachnotron"],
        modifiers=[{"unit_id": "immortal", "stat": "unlock", "value": True}]
    ),

    # Upgrades for Rover - Mutually Exclusive Choice
    "upgrade_rover_speed_1": TechNode(
        id="upgrade_rover_speed_1",
        name="Turbo Charged Engine",
        description="Increases Rover speed by 1.0.",
        type="upgrade",
        prerequisites=["unlock_rover"],
        mutually_exclusive_with=["upgrade_rover_armor_1"],
        modifiers=[{"unit_id": "rover", "stat": "speed", "value": 1.0, "operation": "add"}]
    ),
    "upgrade_rover_armor_1": TechNode(
        id="upgrade_rover_armor_1",
        name="Reinforced Plating",
        description="Increases Rover HP by 20.",
        type="upgrade",
        prerequisites=["unlock_rover"],
        mutually_exclusive_with=["upgrade_rover_speed_1"],
        modifiers=[{"unit_id": "rover", "stat": "hp", "value": 20, "operation": "add"}]
    ),

    # Upgrades for Arachnotron
    "upgrade_arachnotron_range_1": TechNode(
        id="upgrade_arachnotron_range_1",
        name="Targeting Array",
        description="Increases Arachnotron attack range by 2.",
        type="upgrade",
        prerequisites=["unlock_arachnotron"],
        modifiers=[{"unit_id": "arachnotron", "stat": "attack_range", "value": 2, "operation": "add"}]
    ),
}

# Mission Rewards Definition (Potential choices)
MISSION_CHOICES: Dict[str, List[str]] = {
    "mission_1": ["upgrade_rover_speed_1", "upgrade_rover_armor_1"],
    "mission_2": ["unlock_arachnotron"], # Only one choice (forced unlock) or maybe add an alternative?
    # Let's make Mission 2 a choice too for the sake of the roguelike feel
    # "mission_2": ["unlock_arachnotron", "unlock_observer"],
    # But for now, let's stick to simple unlock + upgrade choice.
}
