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

## 2024-05-24 - Clarity over Brevity in Unit Info
**Learning:** The UI was using single-character icons (e.g., "R") in the info panel to match the map representation. While efficient for the map, this increases cognitive load in the detailed info panel where space is not constrained.
**Action:** Use full names (e.g., "Rover") in detailed views/tooltips while keeping icons for the map. If a "display name" is available, prefer it over the raw identifier or icon.
## 2024-05-24 - Animated Text and Caching Performance
**Learning:** Pygame's `lru_cache` on text rendering functions can be inefficient if the color changes every frame (like in a pulse animation), but for low-element count menus, the performance impact is negligible compared to the UX gain.
**Action:** When animating text colors, ensure the number of unique color states or the number of animated elements is low to avoid thrashing the cache.
## 2024-05-23 - Unified Pulse Effect in Settings Scene
**Learning:** Users subconsciously expect consistent feedback mechanisms across similar UI contexts. The static selection state in the Settings menu felt lifeless compared to the Main Menu's pulsing effect, creating a subtle disconnect in the design language.
**Action:** Always verify that visual feedback for interaction states (hover, selection, active) is consistent across all screens. When implementing a new screen, cross-reference existing screens for established patterns like animation curves or color shifts.

## 2024-05-24 - Event-Driven Visual Effects
**Learning:** Visual feedback (like floating damage text) often requires data from logic systems (Combat) but rendering in UI systems. Direct coupling creates spaghetti code. The Event Queue pattern is perfect here: Combat logic emits a "visual_effect" event, and the Scene routes it to the UI.
**Action:** When adding new visual feedback triggered by game logic (e.g., healing numbers, level up flash), use `game_state.add_event({"type": "visual_effect", ...})` instead of calling UI methods directly.

## 2026-05-23 - Escape Navigation and Interactive Cursors
**Learning:** The 'Escape' key is heavily ingrained in gamer muscle memory for pausing, backing out, or quitting. If a full-screen scene lacks an explicit back button, users instinctively press Escape. Furthermore, if a scene is interactive anywhere (click-to-continue), setting a hand cursor once in `__init__` is fragile due to `SceneManager.switch_to` resetting cursors to arrows globally.
**Action:** 1. Always map `pygame.K_ESCAPE` to logical "Back" or "Skip" actions in full-screen unskippable prompts or end screens. 2. Bind cursor changes (e.g., `pygame.SYSTEM_CURSOR_HAND`) to `pygame.MOUSEMOTION` inside the scene's event handler, ensuring the visual affordance persists dynamically rather than relying on a brittle initialization state.
## 2026-05-22 - Accurate Tooltip Width Calculation
**Learning:** Pygame's `pygame.font.Font.size` provides exact text dimensions, replacing inaccurate character-count heuristics (`len(line) * multiplier`) for dynamic content like tooltips.
**Action:** Always use `font.size(text)` when determining the bounding box for rendered text to ensure visual precision and avoid truncation or unnecessary whitespace.
## 2026-05-24 - Consistent Helper Text Guidance
**Learning:** Pygame menus lacking contextual "helper text" can leave users guessing about the exact nature of options (e.g., "Continue Campaign" vs "New Game"). Using a pattern established in the `SettingsScene`, adding descriptive text to the `MenuScene` significantly boosts discoverability and accessibility.
**Action:** When creating or modifying full-screen menus, define a dictionary mapping options to descriptive helper text strings. Render the string corresponding to the currently selected option consistently at the bottom of the screen to guide user intent and improve the menu's overall UX.

## 2024-05-25 - Rapid Pagination in Scrollable Lists
**Learning:** Scrolling through long lists of files in `FileDialog` using arrow keys one-by-one is tedious. Adding rapid pagination support (`pygame.K_PAGEUP` and `pygame.K_PAGEDOWN`) significantly improves keyboard accessibility and navigation speed in Pygame scrollable UI components.
**Action:** When implementing scrollable lists or menus in Pygame UI components, ensure that keyboard shortcuts for jumping by the maximum visible items (e.g., handling `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` to navigate `+/- self.max_visible_files`) are included to provide a faster and more accessible keyboard navigation experience.
