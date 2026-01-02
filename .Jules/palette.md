# Palette's UX Journal

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
