## 2024-05-23 - Movement System SQRT Optimization
**Learning:** Checking `dist_sq <= step_sq` allows us to safely bypass `math.sqrt()` when an entity reaches its target within the current frame, providing a minor loop optimization without changing functional logic.
**Action:** When updating position loops involving distance checks, calculate `max_step_sq` to conditionally evaluate arrival state before invoking expensive math functions.
