## 2025-12-14 - Pause Screen Clarity & Rendering Hygiene
**Learning:** The "Paused" state was represented merely by text, which can get lost against a busy game background. A semi-transparent overlay provides immediate, global feedback that the game state is frozen. Also, uncovered a double-rendering bug where the UI was drawn twice per frame, likely due to copy-paste errors or logic drift.
**Action:** When implementing modal states (like Pause), always use a full-screen scrim/overlay to reduce cognitive load. Also, audit the main render loop for redundant system calls to ensure performance and visual consistency.

## 2025-12-15 - System Feedback Visibility
**Learning:** Critical game events (construction, tech locks, cheat toggles) were only logged to console, which is invisible in full-screen play. Users need immediate, in-context feedback for their actions.
**Action:** Leverage existing "Chat" or message systems to display transient system notifications (Toasts) directly in the UI, using color coding (Green/Red) to denote success/failure.
