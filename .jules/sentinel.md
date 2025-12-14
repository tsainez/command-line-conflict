# Sentinel's Journal

## 2025-12-14 - Map Editor Path Traversal
**Vulnerability:** Path traversal in Map Editor console fallback mode allowing arbitrary file overwrite (with JSON data) and loading.
**Learning:** Console inputs for file operations are often overlooked when GUI (Tkinter) is the primary path, creating security gaps in fallback mechanisms.
**Prevention:** Always sanitize filenames from user input using `os.path.basename()` before joining with directories, especially in less-tested code paths like fallbacks.
