# Cheat Sheet & Debug Commands

This document lists available cheat codes and debug commands for **Command Line Conflict**.

> **Note:** Most of these commands require `config.DEBUG` to be set to `True` or the game to be run in debug mode.

## Cheat Codes

Type these codes while in-game (keyboard shortcuts):

| Key | Effect | Description |
| :--- | :--- | :--- |
| **F1** | Reveal Map | Toggles Fog of War (Global Vision). |
| **F2** | God Mode | Gives infinite health to player units (implementation varying). |
| **F3** | Add Resources | Adds 1000 minerals (if economy enabled). |
| **F4** | Instant Build | Toggles instant construction/training. |
| **F5** | Kill All Enemies | Destroys all enemy units on the map. |
| **F9** | Debug Info | Toggles debug overlay (FPS, entity count). |
| **TAB** | Switch Player | Switches control between Player 1 and Player 2 (Local PvP/Testing). |

## Chat Commands

Press `ENTER` to open the chat, then type these commands:

| Command | Effect |
| :--- | :--- |
| `/reveal` | Reveals the entire map. |
| `/god` | Toggles invulnerability for your units. |
| `/resources` | Grants 5000 minerals and gas. |
| `/killall` | Kills all enemy units. |
| `/spawn [unit]` | Spawns a unit at mouse cursor (e.g., `/spawn tank`). |

## Debug Keys

| Key | Effect |
| :--- | :--- |
| **P** | Pause Game | Toggles game pause state. |
| **~** (Tilde) | Console | Opens developer console (if implemented). |
| **1-6** | Spawn Units | Spawns specific test units at cursor location (Debug Mode only). |

## Launch Arguments

When running `main.py`:

*   `--debug`: Enables debug mode (logs, cheats).
*   `--level [map_name]`: Loads a specific map directly.
*   `--resolution [w]x[h]`: Sets custom window resolution.

## Map Editor Shortcuts

| Key | Effect |
| :--- | :--- |
| **S** | Save Map | Opens save dialog. |
| **L** | Load Map | Opens load dialog. |
| **M** | Toggle Mode | Switches between Wall/Unit placement modes. |
| **Arrows** | Move Camera | Pans the map view. |
