## 2024-06-11 - [Optimize Pathfinding loop]
**Learning:** In A* pathfinding inner loops, Python's overhead from tuple iteration (`for dx, dy in [(-1, 0), ...]`), attribute access (`self.width`), and dictionary membership checking (`if (nx, ny) in dict:`) causes significant slowdowns. Calling standard library functions like `abs()` inside inner loops also adds overhead compared to inline conditionals.
**Action:** Unroll coordinate loops `for nx, ny in ((cx-1, cy), (cx+1, cy), ...)` to eliminate tuple unpacking and iteration. Cache class properties to local variables before the loop. Use `dict.get((nx, ny), default)` to avoid double dictionary lookups.
## 2024-06-12 - [List Comprehension over Loop Append]
**Learning:** In performance-critical Python paths (like per-frame rendering loops), initializing an empty list and calling `.append()` in a loop introduces significant overhead due to function lookup and execution. In `RenderingSystem.draw`, this slowed down spatial map filtering.
**Action:** Replace empty list initialization and loop `.append()` with list comprehensions. List comprehensions are evaluated in C, avoiding the Python-level function call overhead, making iteration over sparse maps noticeably faster.
## 2024-05-18 - Avoid lambda functions in Python sorts
**Learning:** Using `lambda` functions as keys in list sorts introduces significant Python function call overhead.
**Action:** When sorting performance is critical, generate list items natively in the desired sort order (e.g. flipping tuple elements via list comprehension) and use the native `list.sort()` to invoke the optimized C sorting logic.
## 2024-06-13 - [A* Pathfinding: Loop Unrolling and Inlining]
**Learning:** Python function calls (`abs()`) and tuple unpacking inside tight performance-critical loops (like A* pathfinding inner loops) add significant overhead. By fully unrolling the neighbor check loop and inlining Manhattan distance logic using ternary operators (`dx if dx > 0 else -dx`), we bypass iteration overhead and builtin function call overhead. Pre-processing complex obstacle sets outside the `while` loop prevents redundant set difference calculations.
**Action:** Unroll small loops entirely in extremely hot code paths. Pre-process invariant structures (like obstacle diffs) before the loop. Use inline ternary operators instead of `abs()` or `math.sqrt()` to save microseconds per call, which aggregates into measurable frame-time improvements.
## 2024-06-14 - [Optimize Distance Checks and Vector Math]
**Learning:** In performance-critical vector math (like movement updates and fleeing checks calculated per-entity per-frame), calculating `math.sqrt()` is relatively expensive. Often we only need to know if the distance is below a threshold or non-zero. Additionally, dividing multiple coordinate deltas (`dx / dist`, `dy / dist`) introduces redundant division overhead.
**Action:** Replace `math.sqrt()` with squared distance calculations (`dist_sq = dx * dx + dy * dy`) and compare against squared thresholds for early exits. When square roots are necessary, calculate them once and pre-calculate a multiplication ratio (`step_ratio = (speed * dt) / dist`) to apply to all coordinate deltas.
## 2024-06-24 - [Optimize Win/Loss Checks with Early Return]
**Learning:** When iterating over ECS entities or standard lists to evaluate boolean satisfaction (e.g., win/loss checks), accumulating a total count evaluates every entity unnecessarily. This makes checking game over conditions O(N) where N is the total number of units.
**Action:** Use an early return (`return False/True`) upon finding the first match instead of accumulating a total count. This converts an O(N) operation to O(1) in the average case.
## 2024-06-27 - [Early Return in Boolean Satisfaction Checks]
**Learning:** In win/loss condition checks or similar boolean satisfaction queries over entities, accumulating a total count before evaluation results in an unnecessary O(N) operation.
**Action:** Use an early return (e.g., `return False`) upon finding the first match instead of counting all occurrences. This changes the operation from O(N) to O(1) in the average case and improves frame-time performance when many entities are present.
## 2024-06-25 - [Optimize Win/Loss Checks with Early Return]
**Learning:** When iterating over ECS entities or standard lists to evaluate boolean satisfaction (e.g., win/loss checks), accumulating a total count requires evaluating every entity, resulting in an O(N) operation.
**Action:** Replace counting loops with an early return (`return False/True`) upon finding the first match. This converts the O(N) operation into an O(1) operation in the average case during gameplay.
## 2024-06-18 - [Optimize ECS Boolean Checks]
**Learning:** Iterating over ECS entities to evaluate boolean satisfaction (like checking if any enemies are alive for a win/loss condition) by accumulating a total count causes unnecessary O(N) overhead per frame, especially when there are many entities.
**Action:** Use an early return (`return False/True`) upon finding the first match to short-circuit the loop. This converts the O(N) operation to O(1) in the average case and improves frame time during the update loop.

## 2025-05-18 - Use spatial hashing for entity proximity lookups
**Learning:** When needing to find entities that overlap or are near specific coordinates (like factories checking for overlapping units), iterating over all entities (even if filtered by component type) is O(N) and creates O(N*M) bottlenecks.
**Action:** Use `game_state.get_entities_at_position(x, y)` which provides O(1) lookups via the spatial hash map, reducing overall complexity to O(M).
