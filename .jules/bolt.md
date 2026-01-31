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

## 2025-05-27 - UI Text Caching Pattern
**Learning:** Initializing new `pygame.font.Font` objects every frame (even if they use the default system font) causes significant performance degradation. Coupled with uncached `render` calls for static UI text, this can consume a large portion of the frame budget.
**Action:** Always initialize fonts in `__init__` and use `@functools.lru_cache` for text rendering methods in UI systems.

## 2025-05-28 - Loop Hoisting in Rendering
**Learning:** Hoisting constant calculations (like grid size and screen coordinate conversions) out of inner loops in rendering systems can provide significant speedups (e.g., ~45%) by reducing arithmetic operations per entity.
**Action:** Pre-calculate screen coordinates for tiles in the outer loop instead of re-calculating them for every entity in the tile.

## 2025-05-29 - Spatial Lookups for Selection
**Learning:** Iterating over all entities to find what was clicked is O(N) and redundant when a spatial hash map exists. `get_entities_at_position` provides O(1) access. Similarly, iterating only components of interest (e.g., `Selectable`) reduces overhead for global operations like drag selection.
**Action:** Always prefer spatial lookups or component-specific iterators over iterating `game_state.entities.items()` when possible.

## 2025-05-30 - Reducing Lookups in Hot Loops
**Learning:** In nested loops (like rendering grids), re-querying data structures (e.g., `spatial_map.get((x,y))`) inside helper functions adds unnecessary overhead. Passing the retrieved data directly to the helper avoids redundant hash lookups.
**Action:** Extract data in the outer loop and pass it down to helper methods to minimize repeated lookups.
