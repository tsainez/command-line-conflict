## 2024-06-11 - [Optimize Pathfinding loop]
**Learning:** In A* pathfinding inner loops, Python's overhead from tuple iteration (`for dx, dy in [(-1, 0), ...]`), attribute access (`self.width`), and dictionary membership checking (`if (nx, ny) in dict:`) causes significant slowdowns. Calling standard library functions like `abs()` inside inner loops also adds overhead compared to inline conditionals.
**Action:** Unroll coordinate loops `for nx, ny in ((cx-1, cy), (cx+1, cy), ...)` to eliminate tuple unpacking and iteration. Cache class properties to local variables before the loop. Use `dict.get((nx, ny), default)` to avoid double dictionary lookups.
## 2024-06-12 - [List Comprehension over Loop Append]
**Learning:** In performance-critical Python paths (like per-frame rendering loops), initializing an empty list and calling `.append()` in a loop introduces significant overhead due to function lookup and execution. In `RenderingSystem.draw`, this slowed down spatial map filtering.
**Action:** Replace empty list initialization and loop `.append()` with list comprehensions. List comprehensions are evaluated in C, avoiding the Python-level function call overhead, making iteration over sparse maps noticeably faster.

## 2024-08-01 - [Avoid Python method call overhead in inner loops]
**Learning:** In highly performant inner loops (like the `A*` pathfinding logic evaluating thousands of neighbor nodes), invoking an instance method (e.g., `self.is_blocked()`) incurs substantial Python call frame overhead.
**Action:** Instead of invoking methods to access simple attributes, inline the logic (e.g., `(nx, ny) in walls`) and pre-cache the attributes (e.g., `walls = self.walls`) to local variables outside the loop to eliminate method lookups and dramatically improve execution time.
