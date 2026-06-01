## 2025-06-01 - Prevent TypeError DoS in Input Validation
**Vulnerability:** Input validation code for Steam achievements in `command_line_conflict/steam_integration.py` checked string length (`len(achievement_name)`) before verifying the input type. If a non-string or non-sequence type was passed, a `TypeError` would crash the integration system.
**Learning:** Python will eagerly evaluate conditions like `len()` if not guarded by short-circuiting type checks. In weakly typed boundaries (like external API wrappers), assuming input types leads to unhandled exception crashes (DoS).
**Prevention:** Always place strict type verification (e.g., `not isinstance(input, str)`) as the *first* condition in boolean validation checks to properly leverage Python's short-circuit evaluation.
