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

## 2024-05-23 - Unified Pulse Effect in Settings Scene
**Learning:** Users subconsciously expect consistent feedback mechanisms across similar UI contexts. The static selection state in the Settings menu felt lifeless compared to the Main Menu's pulsing effect, creating a subtle disconnect in the design language.
**Action:** Always verify that visual feedback for interaction states (hover, selection, active) is consistent across all screens. When implementing a new screen, cross-reference existing screens for established patterns like animation curves or color shifts.

## 2024-05-24 - Clarity over Brevity in Unit Info
**Learning:** The UI was using single-character icons (e.g., "R") in the info panel to match the map representation. While efficient for the map, this increases cognitive load in the detailed info panel where space is not constrained.
**Action:** Use full names (e.g., "Rover") in detailed views/tooltips while keeping icons for the map. If a "display name" is available, prefer it over the raw identifier or icon.

## 2024-05-24 - Animated Text and Caching Performance
**Learning:** Pygame's `lru_cache` on text rendering functions can be inefficient if the color changes every frame (like in a pulse animation), but for low-element count menus, the performance impact is negligible compared to the UX gain.
**Action:** When animating text colors, ensure the number of unique color states or the number of animated elements is low to avoid thrashing the cache.

## 2024-05-24 - Event-Driven Visual Effects
**Learning:** Visual feedback (like floating damage text) often requires data from logic systems (Combat) but rendering in UI systems. Direct coupling creates spaghetti code. The Event Queue pattern is perfect here: Combat logic emits a "visual_effect" event, and the Scene routes it to the UI.
**Action:** When adding new visual feedback triggered by game logic (e.g., healing numbers, level up flash), use `game_state.add_event({"type": "visual_effect", ...})` instead of calling UI methods directly.

## 2024-05-24 - Tooltips for Disabled States in Pygame
**Learning:** Pygame UIs often lack native support for conveying why an element is disabled. Users can get confused when a "Save" or "Load" button is unresponsive.
**Action:** Always draw a contextual tooltip with a semi-transparent background near disabled interactive elements when they are hovered to explain the required action (e.g., "Filename required").

## 2024-05-24 - Rapid Pagination in Scrollable Lists
**Learning:** Users navigating long scrollable lists via keyboard often find standard up/down arrow keys tedious. Missing rapid pagination (Page Up/Page Down) hinders accessibility and slows down navigation significantly.
**Action:** When implementing custom scrollable UI components like `FileDialog`, always map `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` to paginate the list by the maximum number of visible items per view.

## 2024-05-25 - Rapid Pagination in Scrollable UIs
**Learning:** Users relying on keyboard navigation in scrollable lists with many items experience friction and slow navigation if they can only move one item at a time using arrow keys.
**Action:** Implement rapid pagination support in all scrollable Pygame UI components by handling `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` events to jump by the maximum number of visible items.

## 2024-05-25 - Rapid Pagination Support in Scrollable UI
**Learning:** For scrollable UI components like `FileDialog` in Pygame, relying solely on line-by-line scrolling (Up/Down arrows) becomes tedious for large lists, hurting keyboard accessibility and navigation speed.
**Action:** Implement rapid pagination support by handling `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` key events. When implementing this, always reuse existing internal list navigation methods (e.g., `_navigate(delta)`) instead of manually manipulating scroll offsets to ensure bounds checking and selection updates remain consistent.

## 2024-06-05 - Rapid Pagination in Scrollable UI
**Learning:** To improve keyboard accessibility and navigation speed in Pygame scrollable UI components, implement rapid pagination support by handling `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` key events.
**Action:** In Pygame UI components like `FileDialog`, use the internal `_navigate(delta)` method for list scrolling and navigation instead of manually calculating and updating state variables like `self.scroll_offset`.

## 2024-06-08 - Rapid Pagination Support in FileDialog
**Learning:** For scrollable UI elements handling large lists (e.g., FileDialog), step-by-step navigation with Arrow Up/Down is insufficient and slow. Users expect standard rapid navigation keys like PageUp/PageDown to jump visually by screenfuls.
**Action:** When implementing or modifying scrollable lists, handle `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN`. Use the internal navigation logic (like `_navigate(delta)`) passing the max visible item count (e.g., `-self.max_visible_files` or `self.max_visible_files`) to achieve consistent pagination without duplicating bounds checking or scrolling logic.

## 2024-06-18 - Rapid Pagination in Scrollable Lists
**Learning:** Keyboard navigation in scrollable Pygame UI components (like `FileDialog`) can feel slow when users must press up/down for every single item, degrading accessibility and user experience.
**Action:** Implement rapid pagination support by handling `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` to jump by the maximum visible items (`max_visible_files`), significantly speeding up navigation.

## 2024-06-20 - Rapid Pagination in Scrollable UI
**Learning:** Users navigating long lists in Pygame scrollable components struggle with single-step navigation. Implementing rapid pagination with PAGEUP/PAGEDOWN drastically improves accessibility and keyboard navigation speed.
**Action:** Always implement `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` using the existing navigation delta mechanisms (e.g., `self._navigate(-self.max_visible_files)`) in scrollable UI components like FileDialog.

## 2024-06-23 - Rapid Pagination in Scrollable UI
**Learning:** Pygame scrollable list components without native OS scrollbars can be tedious to navigate with just arrow keys, especially for long lists like file dialogs.
**Action:** Implement `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` support using the internal navigation delta logic scaled to `max_visible_items` to significantly improve keyboard accessibility and navigation speed.

## 2024-06-24 - Rapid Pagination Keyboard Support
**Learning:** Users navigating long file lists using standard arrow keys find it slow and tedious. Implementing Page Up and Page Down keyboard support significantly improves keyboard accessibility and navigation speed in scrollable Pygame UI components.
**Action:** Always implement Page Up/Page Down rapid pagination support (jumping by max visible items) alongside standard up/down arrows in any scrollable list component to improve keyboard accessibility.

## 2026-05-22 - Accurate Tooltip Width Calculation
**Learning:** Pygame's `pygame.font.Font.size` provides exact text dimensions, replacing inaccurate character-count heuristics (`len(line) * multiplier`) for dynamic content like tooltips.
**Action:** Always use `font.size(text)` when determining the bounding box for rendered text to ensure visual precision and avoid truncation or unnecessary whitespace.

## 2026-05-23 - Escape Navigation and Interactive Cursors
**Learning:** The 'Escape' key is heavily ingrained in gamer muscle memory for pausing, backing out, or quitting. If a full-screen scene lacks an explicit back button, users instinctively press Escape. Furthermore, if a scene is interactive anywhere (click-to-continue), setting a hand cursor once in `__init__` is fragile due to `SceneManager.switch_to` resetting cursors to arrows globally.
**Action:** 1. Always map `pygame.K_ESCAPE` to logical "Back" or "Skip" actions in full-screen unskippable prompts or end screens. 2. Bind cursor changes (e.g., `pygame.SYSTEM_CURSOR_HAND`) to `pygame.MOUSEMOTION` inside the scene's event handler, ensuring the visual affordance persists dynamically rather than relying on a brittle initialization state.

## 2026-05-24 - Consistent Helper Text Guidance
**Learning:** Pygame menus lacking contextual "helper text" can leave users guessing about the exact nature of options (e.g., "Continue Campaign" vs "New Game"). Using a pattern established in the `SettingsScene`, adding descriptive text to the `MenuScene` significantly boosts discoverability and accessibility.
**Action:** When creating or modifying full-screen menus, define a dictionary mapping options to descriptive helper text strings. Render the string corresponding to the currently selected option consistently at the bottom of the screen to guide user intent and improve the menu's overall UX.

## 2026-05-25 - Rapid Pagination in Scrollable Lists
**Learning:** For users with many files or items in a list, navigating one-by-one via the arrow keys is tedious and frustrating. Adding rapid pagination support via Page Up and Page Down keys significantly improves keyboard accessibility and navigation speed in scrollable UI components.
**Action:** In Pygame UI components like `FileDialog`, handle `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN` key events to jump by the maximum visible items (e.g., using an internal `_navigate(delta)` method).

## 2026-05-25 - Rapid Pagination Support in FileDialog
**Learning:** For scrollable lists that can grow significantly (like save files or levels), standard arrow-key navigation (up/down one item at a time) becomes tedious and a barrier to efficient keyboard navigation.
**Action:** When implementing or enhancing scrollable UI components, always support rapid pagination using `pygame.K_PAGEUP` and `pygame.K_PAGEDOWN`. Calculate the pagination jump size logically based on the visible view bounds (e.g., jump by `max_visible_files`) and ensure helper text is updated to clearly communicate this capability to the user.
