# CLAUDE.md

This file documents the codebase structure, development workflows, and conventions for AI assistants working on Command Line Conflict.

## Project Overview

Command Line Conflict is an open-source real-time strategy (RTS) game rendered entirely in ASCII art, inspired by StarCraft. Written in Python using pygame, it features an Entity-Component-System (ECS) architecture, AI opponents, fog of war, a built-in map editor, and cross-platform executable builds.

## Tech Stack

- **Python 3.8+** (CI tests 3.10, 3.11, 3.12)
- **pygame** — graphics, input, audio
- **asciimatics** — ASCII animation utilities
- **pillow** — image processing for icon generation
- **pytest + pytest-xdist** — parallel test execution
- **black** (127-char lines), **isort**, **flake8**, **pylint** (min score 9.0), **mypy** — code quality
- **PyInstaller** — executable builds
- **MkDocs + Material theme** — documentation site

## Repository Layout

```
command_line_conflict/   # Main source package
  components/            # ECS Component classes (pure data)
  systems/               # ECS System classes (all logic)
  scenes/                # Game state scenes (menu, game, editor, …)
  maps/                  # Map definitions and file I/O
  ui/                    # UI widgets (file dialog, dev console)
  utils/                 # Utilities (paths, targeting, profiler)
  fonts/                 # Bundled DejaVu font assets
  sounds/                # Audio assets
  engine.py              # Game loop, SceneManager
  game_state.py          # Central ECS state holder
  config.py              # Global constants (grid size, colors, limits)
  factories.py           # Entity creation helpers
  camera.py              # Viewport / camera system
  fog_of_war.py          # Fog of War implementation
  campaign_manager.py    # Campaign / save management
  logger.py              # Rotating file + console logger
  music.py               # Music manager
  steam_integration.py   # Steam API integration
tests/
  conftest.py            # Pytest fixtures; auto-mocks all pygame calls
  unit/                  # Fast isolated tests (components, systems, scenes, …)
  integration/           # End-to-end game flow tests
  security/              # Path traversal, DoS, symlink, TOCTOU tests
docs/                    # MkDocs source (ECS, API, map creation, security)
scripts/
  pre_commit.sh          # Run all checks locally before pushing
  build_windows.ps1      # Windows executable builder
main.py                  # Entry point
build.py                 # PyInstaller build script
```

## Architecture: Entity-Component-System (ECS)

The game uses a strict ECS pattern — see `docs/ECS.md` for a full explanation.

- **Entities** — unique integer IDs (no data, no logic)
- **Components** — plain data classes in `components/` (e.g., `Position`, `Health`, `Attack`)
- **Systems** — logic classes in `systems/` that operate on sets of components each frame

### Accessing components

```python
components = game_state.entities[entity_id]
hp = components.get(Health)            # returns None if missing
pos = components[Position]             # raises KeyError if missing
```

### Querying entities

```python
entities = game_state.get_entities_with_component(Position, Health)
```

### Spatial lookups (O(1))

```python
nearby = game_state.spatial_map[(grid_x, grid_y)]  # set of entity IDs
```

### Creating entities

Use factory helpers in `factories.py`:

```python
entity_id = create_chassis(game_state, x, y, player_id)
entity_id = create_factory(game_state, x, y, player_id)
entity_id = create_wildlife(game_state, x, y)
```

## Development Commands

```bash
# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the game
python main.py

# Run all quality checks (mirrors CI)
./scripts/pre_commit.sh

# Individual checks
black --check .
isort --check-only .
flake8 .
pylint $(git ls-files '*.py')
mypy .
pytest

# Build executables
python build.py                  # cross-platform (PyInstaller)
.\scripts\build_windows.ps1     # Windows-specific
```

## Testing

- **Minimum coverage: 80%** — enforced in CI via `pytest-cov`
- All pygame calls are auto-mocked in `conftest.py`; no display is needed to run tests
- Tests run in parallel (`-n auto`) via `pytest-xdist`
- CI matrix: Ubuntu × Windows × macOS × Python 3.10/3.11/3.12

### Test layout conventions

| Path | Purpose |
|------|---------|
| `tests/unit/components/` | One file per component class |
| `tests/unit/systems/` | One file per system class |
| `tests/unit/scenes/` | One file per scene |
| `tests/integration/` | Multi-system end-to-end flows |
| `tests/security/` | Path traversal, DoS limits, symlink attacks |

When adding a new component, system, or scene, add a matching test file in the appropriate subfolder.

## Code Style & Conventions

### Formatting

- **Black** with 127-character line length — run `black .` before committing
- **isort** with `profile = "black"` — run `isort .` before committing
- Full type annotations throughout; **mypy** must pass with no errors

### Logging

Import the module-level logger and call it directly:

```python
from command_line_conflict.logger import log

log.debug("detailed trace")
log.info("notable event")
log.warning("something unexpected")
```

Do not create per-module loggers; level filtering is handled centrally.

### Configuration constants

Add new global constants to `config.py`. Never hard-code magic numbers for grid size, colors, or limits inline.

Key constants:
- `CELL_SIZE = 20` — pixels per grid cell
- `GRID_WIDTH = 40`, `GRID_HEIGHT = 30` — grid dimensions
- `MAX_ENTITIES = 5000` — DoS protection limit
- `MAX_CHAT_INPUT_LENGTH`, `MAX_FILENAME_LENGTH` — input size limits

### Security requirements

Every place that accepts user-supplied file paths **must** validate against path traversal. Follow the existing pattern in `maps/base.py` and `campaign_manager.py`:

- Resolve the real path with `Path.resolve()`
- Assert it starts with the allowed base directory
- Reject symlinks when appropriate
- Enforce the `.map` extension for map files

The `tests/security/` suite must pass for all new file I/O code.

## CI/CD Pipelines

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `ci.yml` | Every push / PR | Format, lint, type-check, test, docs build |
| `tests.yml` | Every push / PR | Full test matrix (3 OS × 3 Python versions) |
| `deploy_docs.yml` | Push to main | Publish MkDocs site |
| `release.yml` | Tag push | Build executables and create GitHub release |
| `labeler.yml` | PR open | Auto-label by changed paths |
| `stale.yml` | Scheduled | Close stale issues/PRs |

All checks in `ci.yml` must pass before merging. Do not bypass pre-commit hooks.

## Adding New Features

### New component

1. Create `command_line_conflict/components/my_component.py` — data class only, no logic.
2. Add a test in `tests/unit/components/test_my_component.py`.
3. Import and register it wherever entities need it (usually in `factories.py`).

### New system

1. Create `command_line_conflict/systems/my_system.py` — implement `update(game_state, dt)`.
2. Add a test in `tests/unit/systems/test_my_system.py`.
3. Register the system in the `GameScene` (or other scene) system list in `scenes/game.py`.

### New scene

1. Create `command_line_conflict/scenes/my_scene.py` — implement `handle_events`, `update`, `render`.
2. Add a test in `tests/unit/scenes/test_my_scene.py`.
3. Wire the transition in `engine.py`'s `SceneManager`.

### New map

1. Create `command_line_conflict/maps/my_map.py` — subclass `Map` from `maps/base.py`.
2. Override `generate()` to populate the grid.
3. Register it in the editor or game startup as appropriate.

## Known Issues & Backlog

- `AGENTS.md` — AI agent task backlog
- `ISSUES.md` — known bugs and cleanup tasks
- `TODO_ISSUES.md` — specific pending tasks
- `docs/CPP_OPTIMIZATION_STRATEGY.md` — performance improvement roadmap

## Documentation

Source lives in `docs/`. Build and serve locally:

```bash
mkdocs serve        # live-reloading dev server at http://127.0.0.1:8000
mkdocs build        # static output in site/
mkdocs build --strict  # mirrors CI (fails on warnings)
```

Add docstrings to all public classes and functions; `mkdocstrings` generates the API reference automatically.
