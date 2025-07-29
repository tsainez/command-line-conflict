# Project Structure

The project is structured as a Python package. The source code lives in the `command_line_conflict` directory.

```
command_line_conflict/
├── __init__.py
├── config.py      # constants
├── engine.py      # Game class and loop
├── fonts/         # font files
│   └── DejaVuSansMono.ttf
├── maps/          # level definitions
│   ├── __init__.py
│   ├── base.py
│   ├── simple_map.py
│   └── wall_map.py
└── units/
    ├── __init__.py
    ├── base.py    # Unit class
    ├── air_units.py
    ├── airplane.py
    └── ground_units.py
main.py             # entry point
```
