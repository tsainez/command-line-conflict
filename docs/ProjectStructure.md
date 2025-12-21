# Project Structure

The project is structured as a Python package. The source code lives in the `command_line_conflict` directory.

```
.
├── command_line_conflict/   # Core game package (ECS engine, rendering, audio, utilities)
│   ├── components/          # Entity components such as position, health, attack, and vision
│   ├── systems/             # ECS systems (movement, combat, rendering, UI, AI, etc.)
│   ├── scenes/              # Game scenes including menu, game loop, editor, victory/defeat screens
│   ├── maps/                # Map base class and built-in map definitions
│   ├── factories.py         # Entity and component factory helpers
│   ├── engine.py            # Main ECS/game loop orchestration
│   └── config.py            # Shared configuration values
├── tests/                   # Automated tests for game logic and utilities
├── scripts/                 # Development scripts (linting, formatting, docs tooling)
├── docs/                    # Project documentation (MkDocs site content)
├── main.py                  # Command-line entry point for running the game
└── build.py                 # Build helper for packaging and distribution
```
