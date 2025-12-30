# Bolt's Journal

## 2024-05-22 - Spatial Hash Map Efficiency
**Learning:** Using a spatial hash map for collision detection and entity lookup significantly improves performance over O(N) iteration, especially as the entity count grows.
**Action:** Always look for opportunities to replace linear searches with spatial indexing in systems that query entity positions frequently (e.g., collision, vision, targeting).

## 2024-05-23 - Text Rendering Caching
**Learning:** `pygame.font.render` is an expensive operation. Caching rendered text surfaces (especially for static UI elements or frequently recurring text) reduces frame time drastically.
**Action:** Implement LRU caching for text rendering in UI systems.

## 2024-05-24 - Fog of War Optimization
**Learning:** Per-tile drawing for Fog of War is extremely slow in Pygame. Using `pygame.PixelArray` for direct buffer manipulation and scaling a smaller surface is orders of magnitude faster.
**Action:** Prefer surface manipulation and scaling over drawing thousands of individual rects for grid-based visual effects.

## 2024-05-24 - Zero-Copy Pathfinding
**Learning:** Passing `GameState.spatial_map` directly to `Map.find_path` as `extra_obstacles` avoids the overhead of constructing a new set of obstacles every frame, which was an O(N) operation.
**Action:** Pass existing data structures to expensive algorithms instead of rebuilding them, whenever possible.

## 2025-02-14 - List Allocations in Hot Paths
**Learning:** Avoid `list()` conversion when iterating over sets in performance-critical loops (like `CombatSystem.update`) unless snapshot behavior is strictly required for safety (e.g., removing elements from the set during iteration).
**Action:** Iterate over sets directly when safe to avoid O(N) allocation overhead.
