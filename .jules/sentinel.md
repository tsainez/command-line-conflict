## 2026-01-06 - [TOCTOU Vulnerability in File Loading]
**Vulnerability:** A Time-of-Check to Time-of-Use (TOCTOU) race condition existed in `CampaignManager.load_progress`. The code checked the file size with `os.path.getsize` before opening it. An attacker could swap the file for a massive one between the check and the read, causing memory exhaustion (DoS).
**Learning:** Checking a file's properties (like size) and then opening it in a separate step is inherently insecure against race conditions. The state of the file system can change at any moment.
**Prevention:** Always enforce constraints *during* the read operation. Use `f.read(limit)` instead of trusting a pre-check. This "atomic" approach ensures the constraint is respected regardless of external changes.

## 2026-01-10 - [TOCTOU in Map Loading]
**Vulnerability:** Similar to the CampaignManager issue, `Map.load_from_file` checked `os.stat` on a path before opening it. This allowed swapping the file (e.g., via symlink) to bypass size and type checks (like `/dev/zero` or huge files).
**Learning:** Using `os.fstat(f.fileno())` on an open file descriptor is the correct pattern to validate file properties securely. It ensures the checks apply to the exact file object that will be read.
**Prevention:** Open the file first, get the file descriptor, run `os.fstat`, and only then proceed to read.

## 2026-01-14 - [Crash via Unvalidated Map Data]
**Vulnerability:** `Map.from_dict` assumed input keys (`width`, `height`) existed and were valid, leading to `KeyError` or `TypeError` crashes when loading malformed map files.
**Learning:** `from_dict` methods often trust their input too much, assuming they come from a trusted `to_dict` source. However, when loading from files, the input is untrusted user data.
**Prevention:** Always validate existence and types of keys in deserialization methods before using them. Raise handled exceptions (like `ValueError`) instead of letting runtime errors crash the application.
## 2026-01-17 - [Atomic File Writes for Data Integrity]
**Vulnerability:** Direct writes to important data files (save games, maps) using `open(..., 'w')` were vulnerable to data corruption if the process crashed or disk filled up during the write operation. This compromised data integrity and availability.
**Learning:** Python's standard `json.dump` does not guarantee atomicity. A crash mid-write leaves a truncated, invalid JSON file.
**Prevention:** Implemented `atomic_save_json` in `utils/paths.py`. This utility writes to a temporary file first, ensures it is flushed to disk (`os.fsync`), and then uses `os.replace` to atomically swap it with the target file. This pattern should be used for all critical file writes.
## 2026-01-13 - [Source Code Overwrite via Allowed Directories]
**Vulnerability:** `Map.save_to_file` allowed saving to the application source directory (`maps_dir`) to support local development. However, it did not enforce file extensions, allowing an attacker (or compromised UI) to overwrite critical python source files (e.g., `__init__.py`) with JSON data, causing Denial of Service or potentially corrupting the installation.
**Learning:** Allowing an application to write to its own source/installation directory is risky. Even with directory restrictions, failing to enforce file extensions can turn a file-write feature into a destructive capability.
**Prevention:** Strictly enforce file extensions (allowlist) for all user-generated content. Ideally, restrict write operations *only* to isolated user data directories, treating the application directory as read-only.

## 2026-02-01 - [Enforcing Read-Only Application Directory]
**Vulnerability:** Allowing the application to write to its own source directory (`maps_dir`) creates a risk of code overwrite or integrity violation, even with extension checks.
**Learning:** Enforcing a strict "write only to user data" policy requires updating all default paths in the UI (e.g., Editor) to prevent usability regressions. Security restrictions often necessitate UX changes.
**Prevention:** Removed `maps_dir` from `allowed_dirs` in `Map.save_to_file` and updated `EditorScene` to default to `user_data_dir`.
## 2026-05-10 - [Cheat Mode Bypass]
**Vulnerability:** The developer cheats (F1 for reveal map, F2 for god mode) in GameScene were not gated by the DEBUG configuration flag.
**Learning:** Even if a feature is intended only for development, it must be explicitly protected by a configuration check. Otherwise, it might be accessible in production builds.
**Prevention:** Wrap all debug and cheat functionalities in a check against the relevant configuration flag (e.g., `if config.DEBUG:`).
## 2025-05-20 - Unsanitized External API Input
**Vulnerability:** The application passed user-controllable input (`achievement_name`) directly to an external API (`self.steam.SetAchievement()`) without any validation or sanitization.
**Learning:** Even when the implementation of an external library is unknown or abstracted away, it is a critical defense-in-depth practice to validate and constrain all input parameters before passing them across the trust boundary.
**Prevention:** Implement explicit input validation for all parameters passed to external APIs, enforcing a strict character allowlist (e.g., regex `^[A-Za-z0-9_]+$`) and a reasonable length limit.
## 2026-05-24 - [Fix TypeErrors and Prevent Injection in Steam Integration]\n**Vulnerability:** The `unlock_achievement` function assumed its `achievement_name` argument was always a string when evaluating length and regex matching, which could crash the game if non-string types were inadvertently supplied. While the impact is primarily DoS (crashing) or unexpected behaviour, it lacked robust type validation before string operations.\n**Learning:** Relying on implicit typing in dynamically-typed parameters within critical integration points is fragile and vulnerable to both crashes and unexpected behaviors if data sources feed unexpected types.\n**Prevention:** Apply a strict type-check (`isinstance(val, str)`) using short-circuit `or` logic *before* executing string-specific methods like `len()` or `re.match()`. This should be universally applied to all integration boundaries.
## 2024-06-03 - [Fix TOCTOU vulnerability in map file loading]
**Vulnerability:** A Time-of-Check to Time-of-Use (TOCTOU) vulnerability where `os.fstat(f.fileno()).st_size` was used to validate file size before reading it via `json.load(f)`.
**Learning:** File size could be changed between check and read, or special files might misreport size. Using `os.stat` or `fstat` before a read operation without enforcing limits on the read stream itself introduces a security risk (e.g. DoS by memory exhaustion).
**Prevention:** To prevent TOCTOU race conditions in file loading operations, do not pre-check file sizes using `os.path.getsize` or `os.fstat().st_size`. Instead, enforce size constraints atomically during the read operation using `content = f.read(limit)` and checking `len(content)`.
## 2024-06-03 - [Mocking f.read in TOCTOU tests]
**Vulnerability:** Not a direct vulnerability, but a testing failure related to TOCTOU prevention.
**Learning:** When migrating from `json.load(f)` to `content = f.read(); json.loads(content)`, the mocked `open()` function must explicitly mock the `.read()` method. If left un-mocked, `.read()` returns a `MagicMock`, which causes `json.loads()` to throw a `TypeError: the JSON object must be str, bytes or bytearray`.
**Prevention:** Always update associated unit tests to reflect the new `f.read()` behavior by explicitly setting `mock_file.read.return_value = "..."`.
## 2024-06-05 - [Side-Switching Authorization Bypass]
**Vulnerability:** A developer cheat to switch player sides (TAB key) was left outside the `config.DEBUG` check, allowing any player in production to take over the opposing side.
**Learning:** Even features intended solely for development testing must be explicitly gated by environment flags to prevent authorization bypasses.
**Prevention:** Strictly enclose all developer shortcuts, cheats, and debug features within `if config.DEBUG:` blocks to prevent production exploitation.
