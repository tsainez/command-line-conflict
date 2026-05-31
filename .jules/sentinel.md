## 2025-05-31 - [TypeError Crash on External API Input]
**Vulnerability:** Input validation checked `len()` before `isinstance(str)`, leading to unhandled `TypeError` crashes if integers or non-length objects were passed to the Steam API achievement handler.
**Learning:** Short-circuit evaluation order matters critically when checking types and attributes. If type constraints aren't evaluated first, subsequent attribute checks will throw unhandled exceptions, leading to DoS.
**Prevention:** Always place strict type checks (`isinstance`) as the first condition in short-circuit evaluations before length or regex checks when validating un-trusted or external inputs.
