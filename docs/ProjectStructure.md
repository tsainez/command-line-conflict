# Project Structure

This document outlines the file organization and key modules of the **Command Line Conflict** repository.

## Directory Layout

*   `command_line_conflict/`: This is the main source code package for the game.
*   `tests/`: Contains all unit and integration tests.
*   `docs/`: Documentation files, served via MkDocs.
*   `scripts/`: Utility scripts for development and maintenance (e.g., pre-commit checks).
*   `.github/`: GitHub Actions workflows and templates.

## Key Modules

### Core
*   `main.py`: The application entry point. It initializes the engine and starts the game loop.
*   `engine.py`: Manages the game loop, scene transitions (`SceneManager`), and core initialization.
*   `game_state.py`: The central data holder for the Entity-Component-System (ECS). It manages entities, components, and the spatial map.

### Game Logic
*   `systems/`: Contains the game logic systems that operate on entities with specific components.
    *   `movement_system.py`: Handles unit movement and pathfinding.
    *   `combat_system.py`: Manages attacks and damage.
    *   `rendering_system.py`: Draws the game state to the screen.
    *   `ui_system.py`: Renders the Heads-Up Display (HUD) and user interface.
*   `components/`: Defines the data components attached to entities (e.g., `Position`, `Health`, `Movable`).
*   `scenes/`: Implements different game states like `MenuScene`, `GameScene`, `VictoryScene`.

### Assets and Configuration
*   `maps/`: Contains map definitions and loading logic.
*   `config.py`: Central configuration file for game constants and settings.
