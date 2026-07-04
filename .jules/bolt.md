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
## 2024-06-21 - [Early returns for win/loss conditions]
**Learning:** Accumulating counts to check if ANY entity exists (e.g. `enemy_count == 0` for win conditions) forces O(N) iteration over all units every frame.
**Action:** Use an early return (`return False`) as soon as the first satisfying entity is found. This converts an O(N) check into O(1) for the average frame.
## 2024-06-19 - [Optimize Boolean Satisfaction Loops with Early Return]
**Learning:** When iterating over ECS entities or standard lists to evaluate boolean satisfaction (e.g., checking if all enemies are defeated or if the player has any units left), accumulating a total count is inefficient. The frame-by-frame loop evaluates this condition continuously. Accumulating forces an O(N) traversal every frame.
**Action:** Use an early return (`return False/True`) upon finding the first match instead of accumulating a total count. This converts an O(N) operation to O(1) in the average case.
## 2024-06-15 - [Early Exit in Boolean Satisfaction Loops]
**Learning:** When iterating over entities or standard lists to evaluate boolean satisfaction (e.g., win/loss conditions), accumulating a total count introduces unnecessary overhead.
**Action:** Use an early return upon finding the first matching element instead of accumulating a total count. This reduces an O(N) operation to O(1) in the average case.
