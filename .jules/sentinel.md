## 2024-06-20 - Prevent Authorization Bypass for Debug Features
**Vulnerability:** A feature allowing players to switch control sides during gameplay (`pygame.K_TAB`) was globally accessible, enabling an authorization bypass and cheating in production builds.
**Learning:** Even if a feature is intended for debugging or testing, simply placing it in the event handler without checking an environment or configuration flag (like `config.DEBUG`) makes it accessible to all end-users. The surrounding code had other debug features gated correctly, but this one slipped through.
**Prevention:** Always verify that developer-only or admin-level features are explicitly wrapped in authorization or environment checks (e.g., `if config.DEBUG:`) and are not left unprotected in public execution paths.
