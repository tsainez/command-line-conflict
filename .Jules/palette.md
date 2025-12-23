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

## 2025-05-25 - Menu Interaction Consistency
**Learning:** Purely keyboard-driven menus in a desktop environment break the user's mental model of "point and click" interaction, especially when switching between game (mouse-heavy) and menu contexts. This creates a jarring disconnect for users expecting standard UI behavior.
**Action:** Ensure all menu scenes support mouse hover for selection and click for activation, mirroring the keyboard navigation logic to provide a consistent and expected experience.

## 2025-12-22 - Hidden Command Feedback
**Learning:** Hidden commands (like hotkeys or debug toggles) without immediate visual feedback create uncertainty and "mode errors" where users forget the current state.
**Action:** Always pair state-changing hotkeys with a toast, chat message, or visual indicator to confirm the action and current state.
