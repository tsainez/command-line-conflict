## 2026-05-10 - Found Cursor Issues
**Learning:** Defeat and Victory scenes do not show mouse cursor or support mouse click. Adding simple mouse cursor state improvements to Defeat and Victory scenes would make them more accessible and user-friendly.
**Action:** Add cursor state handling to Defeat/Victory scenes, or just improve overall cursor UX.
## 2024-05-11 - Pygame Custom Text Inputs Lack Focus Indicators
**Learning:** Custom-built text inputs in Pygame UI systems inherently lack native focus indicators (like blinking cursors). This makes it difficult for users to know if an input field is active and ready for typing, severely impacting keyboard navigation usability.
**Action:** Always manually implement a blinking cursor (e.g., toggled via `pygame.time.get_ticks() % 1000 < 500`) at the end of the text surface in any custom Pygame text input to provide immediate, visible feedback of input focus.
## 2024-05-18 - Full-Screen Pygame Scenes Need Interaction Cues
**Learning:** Pygame scenes like Victory or Defeat screens that are essentially full-screen click-to-continue prompts lack native affordances. Users may not realize the text is actionable or the screen is waiting for input.
**Action:** In Pygame scenes without explicit button components (like full-screen click-to-continue prompts), use subtle visual cues such as pulsing text (via `math.sin(time)`) and changing the cursor to `pygame.SYSTEM_CURSOR_HAND` to clearly indicate interactivity.
