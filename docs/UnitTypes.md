# Unit Types

Units are the controllable entities in the game. All units inherit from the `Unit` class in `command_line_conflict/units/base.py`.

The game's unit design is based on the concept of artificial intelligence, with units having different levels of "smartness" and unique behaviors.

## Unit Attributes

All units share a set of common attributes:

*   `max_hp`: Maximum health points.
*   `attack_damage`: Damage dealt per attack.
*   `attack_range`: The distance from which a unit can attack.
*   `speed`: Movement speed.
*   `vision_range`: The distance a unit can see, revealing the map from the fog of war.
*   `health_regen_rate`: The rate at which a unit regenerates health per second. Defaults to 0.
*   `can_fly`: A boolean indicating if the unit can fly over obstacles.
*   `flee_health_threshold`: A health percentage (0.0 to 1.0) below which a unit will attempt to flee from combat. `None` by default.
*   `flees_from_enemies`: A boolean indicating if a unit will flee when enemies are nearby, regardless of health.

## Unit Types

Here are the currently implemented units:

### Extractor
*   **Icon:** `E`
*   **Description:** A non-combat unit used for harvesting resources. It has no attack capabilities.
*   **Attributes:**
    *   `attack_damage`: 0
    *   `attack_range`: 0

### Chassis
*   **Icon:** `C`
*   **Description:** A basic, cheap, and expendable melee combat unit. It forms the backbone of any ground army.
*   **Attributes:**
    *   `attack_range`: 1 (melee)

### Rover
*   **Icon:** `R`
*   **Description:** A ranged combat unit with a significant drawback: it has no pathfinding ability. It will move in a straight line towards its target and get stuck on any obstacle, requiring careful micromanagement.
*   **Special Behavior:**
    *   No pathfinding.

### Arachnotron
*   **Icon:** `A`
*   **Description:** A powerful and mobile unit that can fly over any terrain, making it excellent for harassing and flanking.
*   **Attributes:**
    *   `can_fly`: True

### Observer
*   **Icon:** `O`
*   **Description:** A fast, flying, unarmed scout unit. It has an exceptionally large vision range, making it perfect for reconnaissance. It is programmed to automatically flee from any enemy that gets too close.
*   **Attributes:**
    *   `attack_damage`: 0
    *   `vision_range`: 15 (Exceptional)
    *   `speed`: 4 (High)
    *   `flees_from_enemies`: True

### Immortal
*   **Icon:** `I`
*   **Description:** A heavy-duty ranged combat unit. It is durable and possesses health regeneration, allowing it to sustain itself in battle. When its health drops to a critical level, its AI will take over and attempt to flee.
*   **Attributes:**
    *   `health_regen_rate`: 2.0
    *   `flee_health_threshold`: 0.2 (Flees below 20% health)
