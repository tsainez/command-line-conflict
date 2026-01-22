# Maps

Maps define the playable area and the units that are initially on it. All maps inherit from the `Map` class in `command_line_conflict/maps/base.py`.

## Included Maps

### SimpleMap

This is the default map. It's a simple, open map with no obstacles.

### WallMap

This map has a horizontal wall with a gap in the middle. It's a good map for testing pathfinding, as ground units will have to go around the wall to reach the other side. Air units, on the other hand, can fly right over it.

## How to Create a New Map

There are three ways to create a new map: using the in-game Editor, creating a JSON file, or creating a Python subclass.

### 1. Using the Map Editor

The easiest way to create a map is using the built-in Editor.

1.  **Launch the Editor**: From the Main Menu, select "Editor".
2.  **Controls**:
    *   **Left Click**: Toggle a wall at the cursor position.
    *   **Arrow Keys**: Move the camera view.
    *   **Mouse Wheel**: Zoom in/out.
    *   **S**: Save the map.
    *   **L**: Load a map.
    *   **ESC**: Return to the Main Menu.
3.  **Saving**: Press `S` to save your map. Maps are saved as `.json` files in `command_line_conflict/maps/custom/` or your user data directory.

### 2. Creating a JSON Map File

You can manually create or edit map files using JSON. The format is simple:

```json
{
  "width": 40,
  "height": 30,
  "walls": [
    [10, 10],
    [10, 11],
    [10, 12]
  ]
}
```

*   `width`: The width of the map in grid cells.
*   `height`: The height of the map in grid cells.
*   `walls`: A list of `[x, y]` coordinates where walls are located.

Save this file with a `.json` extension. You can then load it using the Map Editor or by creating a custom loader in Python.

### 3. Programmatic Map Creation (Python Subclass)

For more dynamic maps (e.g., procedural generation), you can subclass `Map`.

1.  Create a new file in `command_line_conflict/maps/`.
2.  Import `Map` from `command_line_conflict.maps.base`.
3.  Create a class inheriting from `Map`.
4.  In `__init__`, call `super().__init__(width, height)` and then add walls using `self.add_wall(x, y)`.

Example:

```python
from command_line_conflict.maps.base import Map

class CheckerboardMap(Map):
    def __init__(self, width=40, height=30):
        super().__init__(width, height)
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.add_wall(x, y)
```

## Loading Custom Maps

Currently, the game mainly loads the `SimpleMap` or `WallMap` for standard missions. To play your custom map, you can load it in the Editor. Future updates will allow selecting custom maps for skirmish games.
