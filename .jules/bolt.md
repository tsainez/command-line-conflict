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

## 2025-05-30 - Map Drawing Optimization
**Learning:** Calling `pygame.font.render` and `pygame.transform.scale` inside the inner rendering loop for static map elements (like walls) causes severe performance degradation, doing O(N) expensive text renders when the result is identical.
**Action:** Always hoist invariant rendering operations (like text rendering and scaling of identical sprites) out of loops. Render once per frame and blit multiple times.

## 2025-05-31 - Fast Distance Calculations
**Learning:** Using the exponentiation operator (`** 2`) for calculating squared distances in performance-critical paths (like nested loops for targeting, combat, or UI rendering) routes through slower C-level `BINARY_POWER` operations.
**Action:** Always prefer explicit multiplication (e.g., `dx * dx + dy * dy`) over exponentiation for squared distances to eliminate the function call overhead.

## 2025-06-01 - Fast Square Root Calculations
**Learning:** While explicit multiplication is faster than exponentiation for squaring (`** 2`), calculating the square root via the exponentiation operator (`** 0.5`) routes through the slower C-level `BINARY_POWER` operations compared to calling `math.sqrt()`. Benchmarks show `math.sqrt()` is noticeably faster.
**Action:** Always prefer `math.sqrt(dx * dx + dy * dy)` over `(dx * dx + dy * dy) ** 0.5` for explicit distance calculations.

## 2025-06-02 - Micro-optimizations for Pathfinding
**Learning:** A* Pathfinding in Python using a priority queue can suffer from significant loop overhead. Indexing lists/tuples (`current[0]`), creating arrays (`[(-1, 0), ...]`), performing property lookups (`self.width`, `self.is_blocked`), and executing double dictionary lookups (`(nx, ny) not in g_score ... g_score[(nx, ny)]`) inside the inner `while` and `for` loops quickly degrade performance on large grids or dense unit populations.
**Action:** Always optimize hot paths like A* by caching instance attributes/methods outside the loop to avoid Python attribute lookup overhead, unrolling coordinates to prevent per-iteration object creation, and utilizing `.get()` for dictionary checks to guarantee single lookups.
