## 2026-05-10 - Found Cursor Issues
**Learning:** Defeat and Victory scenes do not show mouse cursor or support mouse click. Adding simple mouse cursor state improvements to Defeat and Victory scenes would make them more accessible and user-friendly.
**Action:** Add cursor state handling to Defeat/Victory scenes, or just improve overall cursor UX.
## 2024-05-11 - Pygame Custom Text Inputs Lack Focus Indicators
**Learning:** Custom-built text inputs in Pygame UI systems inherently lack native focus indicators (like blinking cursors). This makes it difficult for users to know if an input field is active and ready for typing, severely impacting keyboard navigation usability.
**Action:** Always manually implement a blinking cursor (e.g., toggled via `pygame.time.get_ticks() % 1000 < 500`) at the end of the text surface in any custom Pygame text input to provide immediate, visible feedback of input focus.
## 2026-05-10 - Scene-wide Interactivity Cues
**Learning:** Pygame scenes without explicit button components (like full-screen click-to-continue prompts in Defeat/Victory scenes) leave users guessing if the screen is interactive or frozen.
**Action:** When an entire screen acts as a button, provide visual cues: change the cursor to `pygame.SYSTEM_CURSOR_HAND` and add subtle animations (like pulsing text color via `math.sin(time)`) to the call-to-action to indicate interactivity.
## 2026-05-17 - Missing Escape Key Navigation
**Learning:** Some scenes (Settings, Menu) were missing `pygame.K_ESCAPE` handling, which is a common and expected UX pattern for navigating backwards or quitting in games. This breaks standard keyboard navigation flows.
**Action:** Always map the Escape key to the logical "Back" or "Quit" action in all full-screen menu scenes to provide a consistent and intuitive keyboard navigation experience.
## 2024-05-19 - Test Mocking Global State Pollution
**Learning:** When testing UI enhancements in Pygame (like changing `pygame.mouse.set_cursor`), doing `pygame.mouse.set_cursor = MagicMock()` causes severe test pollution that can cascade to other tests since the module level mock is persistent. It fails the required pre commit steps for CI pipeline since tests pollute one another.
**Action:** Always use `unittest.mock.patch("pygame.mouse.set_cursor")` to temporarily replace Pygame's global cursor setter within the test context to avoid leaking the mock to other tests.
## 2024-05-19 - Global Cursor State Bleeding Across Scenes
**Learning:** Updating a Pygame cursor without resetting it can result in global side effects. `SYSTEM_CURSOR_HAND` used in an end screen will bleed over into a main menu screen if standard scene transition methods don't proactively revert back to `SYSTEM_CURSOR_ARROW`.
**Action:** The SceneManager or the new scene's initialization must reset cursor state, or individual scenes must reset it before initiating scene switching logic.
