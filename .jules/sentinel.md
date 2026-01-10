## 2026-01-06 - [TOCTOU Vulnerability in File Loading]
**Vulnerability:** A Time-of-Check to Time-of-Use (TOCTOU) race condition existed in `CampaignManager.load_progress`. The code checked the file size with `os.path.getsize` before opening it. An attacker could swap the file for a massive one between the check and the read, causing memory exhaustion (DoS).
**Learning:** Checking a file's properties (like size) and then opening it in a separate step is inherently insecure against race conditions. The state of the file system can change at any moment.
**Prevention:** Always enforce constraints *during* the read operation. Use `f.read(limit)` instead of trusting a pre-check. This "atomic" approach ensures the constraint is respected regardless of external changes.

## 2026-01-10 - [TOCTOU in Map Loading]
**Vulnerability:** Similar to the CampaignManager issue, `Map.load_from_file` checked `os.stat` on a path before opening it. This allowed swapping the file (e.g., via symlink) to bypass size and type checks (like `/dev/zero` or huge files).
**Learning:** Using `os.fstat(f.fileno())` on an open file descriptor is the correct pattern to validate file properties securely. It ensures the checks apply to the exact file object that will be read.
**Prevention:** Open the file first, get the file descriptor, run `os.fstat`, and only then proceed to read.
