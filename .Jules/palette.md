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

## 2024-05-23 - Visual Affordance for Hidden Content
**Learning:** In the FileDialog, overflow content was hidden without any visual indicator (like a scrollbar), relying on users knowing they could scroll. This is a common accessibility trap in custom UI systems.
**Action:** Always include visual indicators (scrollbars, "more" arrows, or pagination) when content exceeds the viewable area. Implemented a simple calculated scrollbar for the file list.

## 2024-05-24 - Animated Text and Caching Performance
**Learning:** Pygame's `lru_cache` on text rendering functions can be inefficient if the color changes every frame (like in a pulse animation), but for low-element count menus, the performance impact is negligible compared to the UX gain.
**Action:** When animating text colors, ensure the number of unique color states or the number of animated elements is low to avoid thrashing the cache.

## 2024-05-23 - Unified Pulse Effect in Settings Scene
**Learning:** Users subconsciously expect consistent feedback mechanisms across similar UI contexts. The static selection state in the Settings menu felt lifeless compared to the Main Menu's pulsing effect, creating a subtle disconnect in the design language.
**Action:** Always verify that visual feedback for interaction states (hover, selection, active) is consistent across all screens. When implementing a new screen, cross-reference existing screens for established patterns like animation curves or color shifts.

## 2024-05-24 - Destructive Action Confirmation
**Learning:** Immediate action on destructive keys like ESC (Quit) breaks flow and causes frustration if pressed accidentally. A simple confirmation step significantly reduces error rates without adding friction for intentional users.
**Action:** Implement "double-tap" or explicit confirmation overlays for all destructive actions (Quit, Delete, Reset). Visual feedback (Red text, overlay) is crucial to indicate the "pending" state.
