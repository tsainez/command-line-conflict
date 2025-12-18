## 2024-05-23 - Spatial Hashing for Range Queries
**Learning:** Iterating over all entities for range-based queries (like targeting) is a major bottleneck (O(N^2) behavior when many units are scanning). Using the existing `spatial_map` reduces this to O(K) where K is local density, resulting in a ~5x speedup for 1000 entities.
**Action:** Always prefer spatial lookups (grid iteration) for proximity checks over global entity iteration.

## 2024-05-23 - Global State Pollution in Tests
**Learning:** Mocking global objects (like `logging` handlers) in unit tests without proper cleanup can cause "spooky action at a distance" failures in other tests, especially when running in parallel (xdist). In this case, `test_logger.py` added a Mock handler to the global logger, causing `test_targeting.py` to crash when it tried to compare log levels.
**Action:** Always mock `logging.getLogger` or ensure strict cleanup when testing logging configuration to prevent global state pollution.

## 2024-05-24 - Frustum Culling via Spatial Map
**Learning:** Iterating over all entities in `RenderingSystem.draw` (O(N)) is a scalability bottleneck. Switching to iterating visible grid tiles using `spatial_map` (O(View)) reduced rendering time by ~310x for 10,000 entities, demonstrating that for large worlds with sparse viewports, view-dependent iteration is superior.
**Action:** Use spatial partitioning not just for collision, but also for rendering culling when the world size significantly exceeds the viewport.
