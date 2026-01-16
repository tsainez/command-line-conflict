# Maps

Maps define the playable area and the units that are initially on it. All maps inherit from the `Map` class in `command_line_conflict/maps/base.py`.

## SimpleMap

This is the default map. It's a simple, open map with no obstacles.

## WallMap

This map has a horizontal wall with a gap in the middle. It's a good map for testing pathfinding, as ground units will have to go around the wall to reach the other side. Air units, on the other hand, can fly right over it.

## How to Create a New Map

Creating a custom map is straightforward. Follow these steps to add a new battlefield to the game.

### 1. Create a Python File

Create a new file in `command_line_conflict/maps/` (e.g., `forest_map.py`).

### 2. Subclass `Map`

Inherit from the `Map` class and override the `__init__` method.

```python
from .base import Map

class ForestMap(Map):
    def __init__(self):
        # Initialize with width=40, height=30
        super().__init__(40, 30)
        self.setup_walls()

    def setup_walls(self):
        # Add some trees (walls)
        # Create a dense forest block
        for x in range(5, 15):
            for y in range(5, 15):
                # Leave some paths
                if (x + y) % 3 != 0:
                    self.add_wall(x, y)
```

### 3. Register the Map (Optional)

To make the map selectable in the code (e.g., via command line arguments or menu), you might need to import it in `main.py` or wherever map selection happens.

Currently, maps are often instantiated directly in `main.py`:

```python
# main.py
from command_line_conflict.maps.forest_map import ForestMap

# ...
if args.map == "forest":
    game_map = ForestMap()
```

### 4. Using the Map Editor

Alternatively, you can use the in-game Map Editor to create maps visually.

1.  Launch the game and select **Editor** from the main menu.
2.  Left-click to place walls.
3.  Right-click to remove walls.
4.  Press `S` to save the map to a JSON file.
5.  Press `L` to load a map.

Saved maps are stored in your user data directory or the `maps/` directory and can be loaded via the `Map.load_from_file()` method.
