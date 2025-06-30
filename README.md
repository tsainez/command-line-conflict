# command-line-conflict

A fast-paced, open-source RTS game inspired by Starcraft, rendered entirely in charming ASCII art and designed for cross-platform play.

## Getting Started

This project uses **Python** and `pygame` for its simple and readable implementation. To run the prototype:

1) From your repo root, create & activate a venv  
```
python3 -m venv .venv           # or “python -m venv .venv”  
source .venv/bin/activate       
```

2) Upgrade pip and install requirements  
```
pip install --upgrade pip       
pip install -r requirements.txt  
```

3) (Optional) Run linters/tests  
```
pip install black isort pytest  # needed for optional linting/tests

black --check .  
isort --check-only .  
pytest -q  
```

4) Launch the game  
`python main.py    `              

5) (Optional) Bundle into a single executable with PyInstaller  
```
pip install pyinstaller         
pyinstaller --onefile main.py    
# → dist/main  is your standalone binary  
```

The current prototype lets you left-click and drag to select units and right-click to command them to move on the grid. Press **A** while hovering the mouse over a tile to spawn a new airplane unit.

### Font Support
Unit movement paths use Unicode arrow characters. The engine now bundles
**DejaVu Sans Mono** and attempts to load it on startup. If that fails, it tries
common system monospace fonts like **Courier New** and finally falls back to the
default monospace font with ASCII graphics. If you see placeholder blocks
instead of arrows, ensure the DejaVu font can be loaded or rely on the ASCII
fallback.

## Project Structure
The source code now lives in a package with a dedicated module for units so
additional unit types can be added easily.
```
command_line_conflict/
├── __init__.py
├── config.py      # constants
├── engine.py      # Game class and loop
├── maps/          # level definitions
│   ├── __init__.py
│   ├── base.py
│   └── simple_map.py
└── units/
    ├── __init__.py
    ├── base.py    # Unit class
    └── airplane.py  # example subclass
main.py             # entry point
```

### Spawning Units
Maps manage the list of units in play. To add a unit programmatically, call
`spawn_unit` on the current map:

```python
from command_line_conflict.units import Airplane
from command_line_conflict.maps import SimpleMap

game_map = SimpleMap()
game_map.spawn_unit(Airplane(3, 3))
```

While the game runs, press **A** to spawn a new airplane at the mouse cursor.
