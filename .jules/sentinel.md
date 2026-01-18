## 2026-01-06 - [TOCTOU Vulnerability in File Loading]
**Vulnerability:** A Time-of-Check to Time-of-Use (TOCTOU) race condition existed in `CampaignManager.load_progress`. The code checked the file size with `os.path.getsize` before opening it. An attacker could swap the file for a massive one between the check and the read, causing memory exhaustion (DoS).
**Learning:** Checking a file's properties (like size) and then opening it in a separate step is inherently insecure against race conditions. The state of the file system can change at any moment.
**Prevention:** Always enforce constraints *during* the read operation. Use `f.read(limit)` instead of trusting a pre-check. This "atomic" approach ensures the constraint is respected regardless of external changes.

## 2026-01-10 - [TOCTOU in Map Loading]
**Vulnerability:** Similar to the CampaignManager issue, `Map.load_from_file` checked `os.stat` on a path before opening it. This allowed swapping the file (e.g., via symlink) to bypass size and type checks (like `/dev/zero` or huge files).
**Learning:** Using `os.fstat(f.fileno())` on an open file descriptor is the correct pattern to validate file properties securely. It ensures the checks apply to the exact file object that will be read.
**Prevention:** Open the file first, get the file descriptor, run `os.fstat`, and only then proceed to read.

## 2026-01-13 - [Source Code Overwrite via Allowed Directories]
**Vulnerability:** `Map.save_to_file` allowed saving to the application source directory (`maps_dir`) to support local development. However, it did not enforce file extensions, allowing an attacker (or compromised UI) to overwrite critical python source files (e.g., `__init__.py`) with JSON data, causing Denial of Service or potentially corrupting the installation.
**Learning:** Allowing an application to write to its own source/installation directory is risky. Even with directory restrictions, failing to enforce file extensions can turn a file-write feature into a destructive capability.
**Prevention:** Strictly enforce file extensions (allowlist) for all user-generated content. Ideally, restrict write operations *only* to isolated user data directories, treating the application directory as read-only.
