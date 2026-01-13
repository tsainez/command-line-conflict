## 2024-05-23 - Initial Setup
**Learning:** This is a Python/Pygame-based project using ASCII art, not a web app. Standard web accessibility tools (ARIA, semantic HTML) don't apply directly.
**Action:** Focus on:
- Keyboard navigation improvements within Pygame.
- Visual feedback using colors, animations, or text changes.
- Audio cues (if audio is supported).
- Screen reader support via text-to-speech integration (if feasible) or simply ensuring text is clear.
- "Aria-like" labels for ASCII UI elements (e.g., hover tooltips).

## 2024-05-23 - Cursor Feedback in Pygame
**Learning:** Pygame's `mouse.set_cursor` is critical for desktop-like interactivity (hover states) but fails in headless/dummy video drivers used in CI.
**Action:** When adding mouse interaction features:
1. Use `pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)` for clickable elements.
2. ALWAYS mock `pygame.mouse.set_cursor` in `tests/conftest.py` to ensure CI stability.
3. Reset cursor to `pygame.SYSTEM_CURSOR_ARROW` when leaving the view or closing dialogs to prevent "stuck" hand cursors.

## 2024-05-23 - Visual Affordance for Hidden Content
**Learning:** In the FileDialog, overflow content was hidden without any visual indicator (like a scrollbar), relying on users knowing they could scroll. This is a common accessibility trap in custom UI systems.
**Action:** Always include visual indicators (scrollbars, "more" arrows, or pagination) when content exceeds the viewable area. Implemented a simple calculated scrollbar for the file list.

## 2024-05-23 - ASCII Unit Identification
**Learning:** In an ASCII-based game, relying solely on single characters for units (e.g. 'R', 'A') creates a high cognitive load for new users and poor accessibility. Contextual tooltips are essential for "decoding" the interface.
**Action:** Implemented a hover tooltip system that displays the full unit name and health status when hovering over any unit. Crucially, this system respects "Fog of War" to prevent information leakage, maintaining gameplay integrity while improving UX.
