## 2024-06-20 - Prevent Authorization Bypass for Debug Features
**Vulnerability:** A feature allowing players to switch control sides during gameplay (`pygame.K_TAB`) was globally accessible, enabling an authorization bypass and cheating in production builds.
**Learning:** Even if a feature is intended for debugging or testing, simply placing it in the event handler without checking an environment or configuration flag (like `config.DEBUG`) makes it accessible to all end-users. The surrounding code had other debug features gated correctly, but this one slipped through.
**Prevention:** Always verify that developer-only or admin-level features are explicitly wrapped in authorization or environment checks (e.g., `if config.DEBUG:`) and are not left unprotected in public execution paths.
## 2025-01-20 - Sanitize chat input to prevent UI spoofing and XSS
**Vulnerability:** The in-game chat system echoed raw user input without sanitization, which could lead to UI spoofing or Cross-Site Scripting (XSS) risks.
**Learning:** To prevent XSS or UI spoofing in chat systems and text inputs, always sanitize user-controlled text by escaping HTML characters before echoing, broadcasting, or rendering the data.
**Prevention:** Use html.escape to sanitize all user-controlled text input before processing or displaying it.
