# Unit Types

Units are the controllable entities in the game. All units inherit from the `Unit` class in `command_line_conflict/units/base.py`.

There are two main types of units:

*   **Ground Units:** These units cannot move through walls and must use pathfinding to navigate around them.
*   **Air Units:** These units can fly over walls and other obstacles.

## Ground Units

*   **Marine:** A basic infantry unit.
*   **Tank:** A heavy armored unit.

## Air Units

*   **Airplane:** A basic air unit.
*   **Helicopter:** A versatile air unit.
*   **Jet:** A fast air unit.

## Creating New Units

To create a new unit, you need to create a new class that inherits from either `GroundUnit` or `AirUnit`. You also need to set the `icon` class attribute to a character that will represent the unit on the screen.

For example, here's how you would create a new "Artillery" ground unit:

```python
from .base import GroundUnit

class Artillery(GroundUnit):
    icon = "R"
```
