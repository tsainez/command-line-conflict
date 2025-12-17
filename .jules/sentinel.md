# Sentinel's Journal

## 2025-12-14 - Map Editor Path Traversal
**Vulnerability:** Path traversal in Map Editor console fallback mode allowing arbitrary file overwrite (with JSON data) and loading.
**Learning:** Console inputs for file operations are often overlooked when GUI (Tkinter) is the primary path, creating security gaps in fallback mechanisms.
**Prevention:** Always sanitize filenames from user input using `os.path.basename()` before joining with directories, especially in less-tested code paths like fallbacks.

## 2025-12-15 - Unprotected Cheat Codes & Insecure Defaults
**Vulnerability:** Cheat codes (God Mode, Map Reveal) were accessible in the release build, and Debug Mode was enabled by default.
**Learning:** Hardcoded keybindings for developer tools often bypass configuration checks (`config.DEBUG`) if not explicitly gated. Default configurations tend to favor developer convenience over production security.
**Prevention:** Gate all developer/cheat features behind a configuration flag (e.g., `if config.DEBUG:`). Ensure production configuration defaults to secure settings (`DEBUG = False`).

## 2025-12-16 - Unbounded Map Dimensions DoS
**Vulnerability:** The `Map` class allowed arbitrary dimensions (e.g., 10000x10000), leading to massive memory allocation in the `FogOfWar` system and potential Denial of Service.
**Learning:** Data classes often trust input implicitly, assuming they are used correctly by the system. However, when these classes are hydrated from external files (JSON), they become attack vectors if validation is missing.
**Prevention:** Implement strict validation in `__init__` and deserialization methods (`from_dict`) for all data classes that can be loaded from user-provided files. Enforce reasonable limits (e.g., `MAX_MAP_DIMENSION`).
