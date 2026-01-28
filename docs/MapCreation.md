# How to Create a New Map

Creating a new map in **Command Line Conflict** is straightforward. You simply need to subclass the `Map` class and define your terrain features in the `__init__` method.

## Step-by-Step Guide

### 1. Create a New File

Create a new Python file in `command_line_conflict/maps/`. For example, `my_new_map.py`.

### 2. Subclass `Map`

Import the base `Map` class and create your subclass.

```python
from .base import Map

class MyNewMap(Map):
    """A custom map with a maze layout."""

    def __init__(self) -> None:
        # Initialize the map with specific dimensions (e.g., 40x30)
        super().__init__(width=40, height=30)

        # Add your walls and terrain features here
        self._generate_terrain()

    def _generate_terrain(self) -> None:
        # Example: Add a border of walls
        for x in range(self.width):
            self.add_wall(x, 0)
            self.add_wall(x, self.height - 1)

        for y in range(self.height):
            self.add_wall(0, y)
            self.add_wall(self.width - 1, y)

        # Add a central pillar
        center_x, center_y = self.width // 2, self.height // 2
        self.add_wall(center_x, center_y)
```

### 3. Register Your Map (Optional)

Currently, map loading is handled by importing the map class directly. To make it available in the game, you might need to add it to the map selection logic in `command_line_conflict/scenes/menu.py` or wherever map selection occurs.

## Key Methods

### `add_wall(x, y)`

Adds a wall at the specified grid coordinates. Walls block ground units but allow flying units to pass.

```python
self.add_wall(10, 15)
```

### `is_blocked(x, y)`

Checks if a specific tile is occupied by a wall.

```python
if self.is_blocked(5, 5):
    print("There is a wall here!")
```

## Tips

- **Validation**: The `Map` class automatically checks if walls are within bounds.
- **Performance**: Avoid creating extremely large maps or too many walls, as it might impact pathfinding performance.
- **Testing**: You can test your map by modifying `main.py` to load your new map class instead of the default one, or by using the Map Editor if available.
