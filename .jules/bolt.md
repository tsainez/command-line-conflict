## 2024-05-23 - Spatial Hashing for Range Queries
**Learning:** Iterating over all entities for range-based queries (like targeting) is a major bottleneck (O(N^2) behavior when many units are scanning). Using the existing `spatial_map` reduces this to O(K) where K is local density, resulting in a ~5x speedup for 1000 entities.
**Action:** Always prefer spatial lookups (grid iteration) for proximity checks over global entity iteration.
