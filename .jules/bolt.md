# Bolt Journal
## 2024-05-24 - Frustum Culling via Spatial Map
**Learning:** Iterating over all entities in `RenderingSystem.draw` (O(N)) is a scalability bottleneck. Switching to iterating visible grid tiles using `spatial_map` (O(View)) reduced rendering time by ~310x for 10,000 entities, demonstrating that for large worlds with sparse viewports, view-dependent iteration is superior.
**Action:** Use spatial partitioning not just for collision, but also for rendering culling when the world size significantly exceeds the viewport.

## 2024-05-23 - Spatial Hashing for Range Queries
**Learning:** Iterating over all entities for range-based queries (like targeting) is a major bottleneck (O(N^2) behavior when many units are scanning). Using the existing `spatial_map` reduces this to O(K) where K is local density, resulting in a ~5x speedup for 1000 entities.
**Action:** Always prefer spatial lookups (grid iteration) for proximity checks over global entity iteration.

## 2024-05-23 - Global State Pollution in Tests
**Learning:** Mocking global objects (like `logging` handlers) in unit tests without proper cleanup can cause "spooky action at a distance" failures in other tests, especially when running in parallel (xdist). In this case, `test_logger.py` added a Mock handler to the global logger, causing `test_targeting.py` to crash when it tried to compare log levels.
**Action:** Always mock `logging.getLogger` or ensure strict cleanup when testing logging configuration to prevent global state pollution.

## 2025-12-16 - Python Loop vs C Loop for Set Construction
**Learning:** Iterating over a dictionary in Python to build a set (`for k, v in dict.items(): if ...`) is significantly slower than using the C-optimized `set(dict)` constructor, even if you have to perform a small fix-up afterwards. In `MovementSystem._get_obstacles`, switching to `set(spatial_map)` reduced execution time by ~50% in microbenchmarks.
**Action:** When converting collection types, prefer built-in constructors (`set()`, `list()`) over manual loops whenever possible, handling exceptions/filtering afterwards if the "happy path" covers the majority of cases.

## 2025-12-16 - Duck Typing in Tight Loops
**Learning:** Replacing a standard `set` with a custom "proxy" object (implementing `__contains__`) to lazily calculate membership inside a hot path (like A* pathfinding) degraded performance by ~10-15%. The overhead of Python method calls in the tight inner loop outweighed the savings from avoiding the initial set construction.
**Action:** Avoid complex proxy objects in tight computational loops (like pathfinding or rendering). Pay the upfront cost for a native data structure if the loop count is high.

## 2025-12-19 - FogOfWar Optimization
**Learning:** Iterating over the entire map (O(MapSize)) for Fog of War updates and rendering is a major bottleneck on large maps (e.g., 256x256). By restricting updates to previously visible cells and rendering to the camera viewport, we achieved massive gains.
**Action:**
1. Optimized `update`: Track `visible_cells` to only downgrade relevant tiles (O(Visible)) instead of scanning the whole map.
2. Optimized `update`: Cached vision circle offsets to avoid repeated distance calculations (O(1) lookup vs O(R^2) math).
3. Optimized `draw`: Intersect camera viewport with map bounds to render only visible tiles (O(View) vs O(MapSize)).
**Result:** Reduced FogOfWar processing time from ~27ms to ~10.8ms (60% reduction) on a 256x256 map with 50 units.

## 2025-05-25 - Zero-Copy Pathfinding Obstacles
**Learning:** Avoiding the creation of temporary obstacle sets (O(N)) for A* pathfinding by passing the persistent `spatial_map` directly resulted in a ~20% speedup for short paths.
**Action:** When filtering a large collection for a hot loop, prefer passing the collection reference and a small "exclusion" list rather than copying/modifying the collection.

## 2025-12-22 - Replacing Python Draw Loops with Texture Blitting
**Learning:** Even when culling visible tiles, iterating over 1000+ grid cells in Python to call `pygame.draw` or `surface.fill` is slow (~3ms). Replacing this with a persistent `pygame.Surface` (texture) updated via `PixelArray` (differential updates only) and drawn via `transform.scale` + `blit` (C-level) reduced draw time by ~50% in benchmarks.
**Action:** For grid-based rendering layers (like fog, terrain), maintain a persistent off-screen surface and use blitting instead of per-tile drawing loops.

## 2025-12-23 - Skipping Fog Calculations for Stationary Units
**Learning:** Even with optimized rendering (PixelArray), recalculating the visible set for Fog of War every frame (O(N*R^2)) is wasteful if units haven't moved. Implementing a simple check for changes in unit state (position/range) reduced update time by ~98% (4.5ms -> 0.07ms) for stationary frames.
**Action:** For systems that process the same input repeatedly (like Fog of War or static UI), check if the input state signature has changed before recalculating.
