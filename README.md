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
# black --check .  
# isort --check-only .  
# pytest -q  
```

4) Launch the game  
`python main.py    `              

5) (Optional) Bundle into a single executable with PyInstaller  
```
pip install pyinstaller         
pyinstaller --onefile main.py    
# → dist/main  is your standalone binary  
```

The current prototype lets you left-click and drag to select units and right-click to command them to move on the grid.

## Project Structure
The source code now lives in a package with a dedicated module for units so
additional unit types can be added easily.
```
command_line_conflict/
├── __init__.py
├── config.py      # constants
├── engine.py      # Game class and loop
└── units/
    ├── __init__.py
    ├── base.py    # Unit class
    └── airplane.py  # example subclass
main.py             # entry point
```