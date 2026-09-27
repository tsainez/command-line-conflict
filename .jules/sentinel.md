## 2024-06-20 - Prevent Authorization Bypass for Debug Features
**Vulnerability:** A feature allowing players to switch control sides during gameplay (`pygame.K_TAB`) was globally accessible, enabling an authorization bypass and cheating in production builds.
**Learning:** Even if a feature is intended for debugging or testing, simply placing it in the event handler without checking an environment or configuration flag (like `config.DEBUG`) makes it accessible to all end-users. The surrounding code had other debug features gated correctly, but this one slipped through.
**Prevention:** Always verify that developer-only or admin-level features are explicitly wrapped in authorization or environment checks (e.g., `if config.DEBUG:`) and are not left unprotected in public execution paths.

## 2024-07-31 - Prevent Chat Message Injection / XSS
**Vulnerability:** The in-game chat system directly echoed user input into messages without escaping HTML characters. If messages are broadcasted or logged in external systems (like web interfaces), this allows Cross-Site Scripting (XSS).
**Learning:** Pygame rendering itself is mostly immune to XSS, but UI spoofing (e.g., faking server messages) or downstream processing (like web-based logs) can still be exploited if user input is not sanitized at the source.
**Prevention:** Always sanitize or escape user-controlled text inputs using standard libraries (like `html.escape`) before echoing, broadcasting, or rendering them.
