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
**Vulnerability:** The `Map` class allowed arbitrary width/height, which led to massive memory allocation in the `FogOfWar` system (O(N^2)), causing Denial of Service.
**Learning:** Generic data structures should enforce sensible limits on their dimensions to prevent resource exhaustion, even if the "business logic" implies safety. Trusting input JSON structure blindly allows malformed data to crash the application.
**Prevention:** Implement explicit `MAX_` limits in constructors and deserialization methods (`from_dict`). Validate array dimensions and coordinate bounds during data loading.

## 2025-12-18 - Unbounded List Processing in Map Deserialization
**Vulnerability:** The `Map.from_dict` method iterated over an arbitrarily long list of walls before validating them, allowing CPU exhaustion via malicious JSON files with millions of items.
**Learning:** Validating individual items in a loop is expensive if the input size is unchecked. Resource consumption (CPU) can be attacked even if the final state (memory) is bounded.
**Prevention:** Verify list lengths against expected bounds (e.g., `width * height`) *before* processing elements. Truncate or reject excessive input early.
