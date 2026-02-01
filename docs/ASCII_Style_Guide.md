# ASCII Style Guide

**Command Line Conflict** uses a distinct ASCII art style to represent units, buildings, and the environment. This guide serves as a reference for developers and map creators.

## Entities

Entities are represented by single characters. Their color is determined by the owning player (e.g., Player 1 is typically Green, Player 2 is Red).

### Units

| Unit Name | Character | Description |
| :--- | :---: | :--- |
| **Chassis** | `C` | The basic worker unit. Small and weak. |
| **Rover** | `R` | A fast scout and light attack unit. |
| **Arachnotron** | `A` | A heavy flying combat unit. |
| **Observer** | `O` | A flying scout unit with large vision radius. |
| **Immortal** | `I` | A tanky ground unit with high health. |
| **Extractor** | `E` | A resource gathering unit. |

### Buildings

| Building Name | Character | Description |
| :--- | :---: | :--- |
| **Rover Factory** | `F` | Produces Rovers. |
| **Arachnotron Factory** | `f` | Produces Arachnotrons. |

### Neutral / Environment

| Name | Character | Color | Description |
| :--- | :---: | :--- | :--- |
| **Wildlife** | `w` | Grey | Neutral creatures that wander the map. |
| **Wall** | `#` | Grey (100, 100, 100) | Blocks ground movement. |
| **Confetti** | `*` | Various | Visual effect particles. |

## UI & Overlays

*   **Selection**: Selected units are highlighted with a green rectangle overlay.
*   **Fog of War**: Unexplored areas are black (hidden). Explored but not visible areas are dimmed.
*   **Pathing**: Movement paths are often visualized with lines or arrows if debugging is enabled.

## Design Principles

1.  **Readability**: Characters should be distinct enough to be recognized at a glance.
2.  **Case Sensitivity**: Uppercase usually denotes standard combat units or major buildings. Lowercase denotes smaller or secondary variants (e.g., `f` for advanced factory, `w` for wildlife).
3.  **Contrast**: Colors play a huge role. Ensure player colors contrast well with the black background and grey walls.
