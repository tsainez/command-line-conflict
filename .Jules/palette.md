# Palette Journal
## 2024-05-23 - Command Confirmation Feedback
**Learning:** In spatial interfaces like RTS games, the lack of immediate visual feedback for move commands creates uncertainty ("Did I click correctly?"). Adding a simple ripple effect at the click location provides essential confirmation of the action's success and location.
**Action:** Ensure all point-and-click commands in the game (move, attack, build) trigger a distinct visual response at the target location.

## 2025-12-14 - Pause Screen Clarity & Rendering Hygiene
**Learning:** The "Paused" state was represented merely by text, which can get lost against a busy game background. A semi-transparent overlay provides immediate, global feedback that the game state is frozen. Also, uncovered a double-rendering bug where the UI was drawn twice per frame, likely due to copy-paste errors or logic drift.
**Action:** When implementing modal states (like Pause), always use a full-screen scrim/overlay to reduce cognitive load. Also, audit the main render loop for redundant system calls to ensure performance and visual consistency.

## 2025-05-20 - Context-Aware Health Bars
**Learning:** Color-coding health bars (Green/Yellow/Red) combined with neutral backgrounds drastically improves "at-a-glance" status reading compared to simple foreground/background fills, especially for color-blind users who struggle with Red/Green contrast.
**Action:** Whenever displaying status meters, use multi-stage coloring and high-contrast borders to convey urgency without relying solely on length.

## 2025-12-15 - Input Modality Exclusion
**Learning:** The UI architecture consistently assumes keyboard-only navigation for menus, likely due to CLI/keyboard-centric origins. This excludes mouse/touch users and requires refactoring scene `draw` methods to store layout data (rects) for hit-testing in event handlers.
**Action:** When creating new UI scenes, always separate layout calculation from rendering to facilitate mouse/touch hit-testing without code duplication or "render-to-find" hacks.
