## 2025-12-14 - Pause Screen Clarity & Rendering Hygiene
**Learning:** The "Paused" state was represented merely by text, which can get lost against a busy game background. A semi-transparent overlay provides immediate, global feedback that the game state is frozen. Also, uncovered a double-rendering bug where the UI was drawn twice per frame, likely due to copy-paste errors or logic drift.
**Action:** When implementing modal states (like Pause), always use a full-screen scrim/overlay to reduce cognitive load. Also, audit the main render loop for redundant system calls to ensure performance and visual consistency.

## 2024-05-23 - Command Confirmation Feedback
**Learning:** In spatial interfaces like RTS games, the lack of immediate visual feedback for move commands creates uncertainty ("Did I click correctly?"). Adding a simple ripple effect at the click location provides essential confirmation of the action's success and location.
**Action:** Ensure all point-and-click commands in the game (move, attack, build) trigger a distinct visual response at the target location.
