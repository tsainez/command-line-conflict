# How to Create a New Map

This guide explains how to create new maps for *Command Line Conflict*, either using the in-game editor or by writing a Python class.

## Option 1: Using the Map Editor (Recommended)

The easiest way to create a map is using the built-in Map Editor.

1.  **Start the Game**: Run `python main.py`.
2.  **Enter Editor**: Select "Map Editor" from the main menu.
3.  **Controls**:
    *   **Left Click**: Place a wall.
    *   **Right Click**: Remove a wall.
    *   **Arrow Keys**: Move the camera.
    *   **S**: Save the map.
    *   **L**: Load an existing map.
    *   **ESC**: Exit to menu.
4.  **Saving**: When you press 'S', a dialog will appear. Enter a filename (e.g., `my_new_map`) and click "Save". The map will be saved as a JSON file in your user data directory (usually `~/.local/share/Command Line Conflict/` on Linux).

## Option 2: Defining a Map Class (Advanced)

For more control (e.g., custom starting units, special terrain generation logic), you can define a map as a Python class.

1.  **Create a File**: Create a new file in `command_line_conflict/maps/`, e.g., `my_custom_map.py`.
2.  **Inherit from `Map`**: Subclass the base `Map` class.
3.  **Implement `__init__`**: Set the dimensions and place static walls.
4.  **Implement `create_initial_units` (Optional)**: Define starting units for players.

### Example: `my_custom_map.py`

```python
from command_line_conflict.maps.base import Map
from command_line_conflict import factories

class MyCustomMap(Map):
    def __init__(self):
        # Initialize a 50x50 map
        super().__init__(width=50, height=50)

        # Add a central wall
        for y in range(20, 30):
            self.add_wall(25, y)

    def create_initial_units(self, game_state):
        """Called when the game starts to spawn units."""

        # Spawn Player 1 (Human) start location
        factories.create_chassis(game_state, 5, 25, player_id=1, is_human=True)
        factories.create_extractor(game_state, 3, 25, player_id=1, is_human=True)

        # Spawn Player 2 (AI) start location
        factories.create_rover(game_state, 45, 25, player_id=2, is_human=False)
```

5.  **Register the Map**: To make it playable, you currently need to modify `command_line_conflict/scenes/game.py` to load your map class instead of `FactoryBattleMap`.
    *   *Note: A map selection screen is a planned feature.*

## Option 3: JSON Format

Maps can also be manually created or edited as JSON files.

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

*   **width/height**: Integer dimensions of the grid.
*   **walls**: A list of `[x, y]` coordinates where walls are located.
