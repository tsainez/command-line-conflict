## 2025-12-25 - Unbounded Filename Input DoS
**Vulnerability:** `FileDialog` allowed unlimited string input for filenames, potentially causing memory exhaustion (DoS) or filesystem errors with extremely long paths.
**Learning:** Input fields in UI components, even for internal tools like map editors, must always enforce length limits. Standard libraries (like Pygame) do not enforce these by default.
**Prevention:** Added `MAX_FILENAME_LENGTH` (64 chars) to `config.py` and enforced it in `FileDialog.handle_event`.
