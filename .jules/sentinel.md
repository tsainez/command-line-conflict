## 2025-12-25 - Unbounded Filename Input DoS
**Vulnerability:** `FileDialog` allowed unlimited string input for filenames, potentially causing memory exhaustion (DoS) or filesystem errors with extremely long paths.
**Learning:** Input fields in UI components, even for internal tools like map editors, must always enforce length limits. Standard libraries (like Pygame) do not enforce these by default.
**Prevention:** Added `MAX_FILENAME_LENGTH` (64 chars) to `config.py` and enforced it in `FileDialog.handle_event`.
## 2024-05-23 - Map Path Traversal Protection
**Vulnerability:** The `Map.save_to_file` method in `base.py` allowed arbitrary file writes via path traversal because it did not validate the output directory. While the editor UI sanitized input, direct calls (e.g., from future features or mods) could be exploited.
**Learning:** Security validation should be done as close to the sensitive operation as possible (Defense in Depth), not just at the UI layer. Reliance on caller sanitization is fragile.
**Prevention:** I implemented a check in `Map.save_to_file` using `os.path.commonpath` to enforce that files can only be saved to the authorized `maps/` directory or the user data directory.
