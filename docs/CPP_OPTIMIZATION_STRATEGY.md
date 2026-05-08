# C++ Optimization Strategy for Command Line Conflict

## 1. Performance Bottlenecks Analysis

Based on the review of the core game loop and physics calculations in Python, the following areas have been identified as the most significant performance bottlenecks:

### A* Pathfinding (`command_line_conflict/maps/base.py`)
The `find_path` method implements the A* algorithm in pure Python. It uses a `heapq` for the open set and multiple dictionaries for `came_from` and `g_score`. During gameplay, particularly when many intelligent units (e.g., enemies or player units) request pathfinding simultaneously, the Python overhead of iterating through nodes, calculating heuristics (Manhattan distance), and updating dictionaries and lists is high. This can cause significant frame drops and stuttering.

### Combat System Distance Calculations (`command_line_conflict/systems/combat_system.py`)
The `CombatSystem.update` method iterates over all entities with an `Attack` component. Inside the loop, it computes the squared distance between the attacker and its target. While it correctly avoids the expensive `math.sqrt()` by comparing squared distances (`dist_sq <= attack_range_sq`), iterating over potentially hundreds of entities per frame in Python introduces a baseline overhead that scales poorly with unit count.

### Movement System Updates (`command_line_conflict/systems/movement_system.py`)
The `MovementSystem.update` also iterates over all movable entities every frame. It calculates step distances and does collision checks (`is_position_occupied`). The frequent function calls, object attribute access (`movable.target_x`, `position.y`), and collision checking logic in Python can bottleneck the game when the entity count grows.

### Python Object Overhead & Core Loop (`command_line_conflict/engine.py`)
The main loop in `Game.run()` calls updates for all systems sequentially. The overhead of Python function calls, dictionary lookups for ECS components (`game_state.entities.get(entity_id)`), and dynamic typing overhead limit the maximum entity processing throughput.

## 2. C++ Rewrite Strategy

To dramatically improve runtime efficiency while maintaining the existing logic, we propose rewriting the identified high-cost functions in C++ and exposing them to Python using **pybind11**.

### Migration Plan
1.  **Phase 1: Pathfinding (Highest Priority)**
    *   Implement the A* algorithm in C++ using `std::priority_queue`, `std::unordered_set`, and `std::unordered_map` (or flat arrays for grid lookup to be even faster).
    *   Expose a `Pathfinder` class to Python using pybind11.
    *   Replace the `find_path` method in `Map` to call the C++ pathfinder.

2.  **Phase 2: Math and Spatial Queries (Medium Priority)**
    *   Move distance calculations and collision detection checks into C++.
    *   Create a spatial hash grid or quadtree in C++ to optimize `is_position_occupied` and closest-target queries.

3.  **Phase 3: System Updates (Long-term)**
    *   For systems like `CombatSystem` and `MovementSystem`, consider adopting a Data-Oriented Design (DOD). We can store component data (positions, velocities, health) in contiguous arrays (Struct of Arrays) in C++.
    *   Python will pass arrays (using `numpy` or `memoryview`) to C++ for batch processing (e.g., `update_positions_and_collisions(positions, velocities, dt)`).

### Why pybind11?
*   **Modern & Lightweight:** It allows writing clean, pure C++11/14/17 code without the boilerplate of raw C-API or Cython syntax.
*   **Performance:** The overhead of crossing the Python/C++ boundary is minimal.
*   **Integration:** Easily integrates with `setuptools` for building the extension module during installation.

## 3. Example Refactored C++ Class: Pathfinder

Below is an example of the first refactored C++ class implementing the A* pathfinding algorithm. This class uses `std::priority_queue` for fast node retrieval and `std::vector` for fast grid lookups instead of hash maps where possible.

```cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <queue>
#include <unordered_set>
#include <unordered_map>
#include <cmath>
#include <tuple>

namespace py = pybind11;

// Helper struct for coordinates
struct Point {
    int x, y;
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

// Hash function for Point to be used in unordered maps/sets
struct PointHash {
    std::size_t operator()(const Point& p) const {
        return std::hash<int>()(p.x) ^ (std::hash<int>()(p.y) << 1);
    }
};

class Pathfinder {
private:
    int width, height;
    std::unordered_set<Point, PointHash> walls;

public:
    Pathfinder(int w, int h, const std::vector<std::pair<int, int>>& wall_coords)
        : width(w), height(h) {
        for (const auto& w_coord : wall_coords) {
            walls.insert({w_coord.first, w_coord.second});
        }
    }

    bool is_blocked(int x, int y) const {
        return walls.find({x, y}) != walls.end();
    }

    std::vector<std::pair<int, int>> find_path(
        std::pair<int, int> start_coord,
        std::pair<int, int> goal_coord,
        bool can_fly,
        const std::vector<std::pair<int, int>>& extra_obstacles,
        const std::vector<std::pair<int, int>>& exclude_obstacles) {

        Point start = {start_coord.first, start_coord.second};
        Point goal = {goal_coord.first, goal_coord.second};

        if (!can_fly && is_blocked(goal.x, goal.y)) {
            return {};
        }

        std::unordered_set<Point, PointHash> extra_obs_set;
        for (const auto& obs : extra_obstacles) extra_obs_set.insert({obs.first, obs.second});

        std::unordered_set<Point, PointHash> exclude_obs_set;
        for (const auto& obs : exclude_obstacles) exclude_obs_set.insert({obs.first, obs.second});

        // Priority Queue elements: <f_score, f_score, Point>
        using PQElement = std::pair<int, Point>;
        auto cmp = [](const PQElement& left, const PQElement& right) {
            return left.first > right.first; // Min-heap
        };
        std::priority_queue<PQElement, std::vector<PQElement>, decltype(cmp)> open_set(cmp);

        std::unordered_map<Point, Point, PointHash> came_from;
        std::unordered_map<Point, int, PointHash> g_score;

        open_set.push({0, start});
        g_score[start] = 0;

        int iterations = 0;
        const int MAX_ITERATIONS = 5000;

        const std::vector<Point> directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        while (!open_set.empty()) {
            iterations++;
            if (iterations > MAX_ITERATIONS) break;

            Point current = open_set.top().second;
            open_set.pop();

            if (current == goal) {
                std::vector<std::pair<int, int>> path;
                while (!(current == start)) {
                    path.push_back({current.x, current.y});
                    current = came_from[current];
                }
                std::reverse(path.begin(), path.end());
                return path;
            }

            for (const auto& dir : directions) {
                Point next = {current.x + dir.x, current.y + dir.y};

                if (next.x < 0 || next.x >= width || next.y < 0 || next.y >= height) continue;

                if (!can_fly && is_blocked(next.x, next.y)) continue;

                if (extra_obs_set.find(next) != extra_obs_set.end()) {
                    if (exclude_obs_set.find(next) == exclude_obs_set.end()) {
                        continue;
                    }
                }

                int tentative_g = g_score[current] + 1;

                if (g_score.find(next) == g_score.end() || tentative_g < g_score[next]) {
                    g_score[next] = tentative_g;
                    int f_score = tentative_g + std::abs(next.x - goal.x) + std::abs(next.y - goal.y);
                    open_set.push({f_score, next});
                    came_from[next] = current;
                }
            }
        }

        return {}; // Return empty path if no path found or iterations exceeded
    }
};

// pybind11 module definition
PYBIND11_MODULE(clc_cpp_core, m) {
    m.doc() = "C++ Core modules for Command Line Conflict";

    py::class_<Pathfinder>(m, "Pathfinder")
        .def(py::init<int, int, const std::vector<std::pair<int, int>>&>())
        .def("find_path", &Pathfinder::find_path,
             py::arg("start"), py::arg("goal"), py::arg("can_fly") = false,
             py::arg("extra_obstacles") = std::vector<std::pair<int, int>>(),
             py::arg("exclude_obstacles") = std::vector<std::pair<int, int>>());
}
```
