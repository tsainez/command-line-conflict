import random

from .base import Map

# [DATA STRUCTURES]
# The base Map class uses a Set[Tuple[int, int]] named `self.walls` to store wall coordinates.
# The grid itself is implicitly defined by `self.width` and `self.height`.


class ProceduralMap(Map):
    """
    [ALGORITHM CORE]
    A procedurally generated map using Cellular Automata to create organic, cave-like structures.
    The algorithm is purely decoupled from the rendering/engine layer and operates on
    abstract map coordinates.
    """

    def __init__(
        self, seed: int = 42, width: int = 40, height: int = 30, fill_probability: float = 0.45, smoothing_iterations: int = 4
    ) -> None:
        """
        Initializes the ProceduralMap and runs the generation algorithm.

        Args:
            seed: Seed value for the deterministic PRNG.
            width: Width of the map.
            height: Height of the map.
            fill_probability: Initial chance for a cell to become a wall.
            smoothing_iterations: Number of passes for the cellular automata.
        """
        super().__init__(width=width, height=height)

        self.seed = seed
        self.fill_probability = fill_probability
        self.smoothing_iterations = smoothing_iterations

        # Initialize deterministic PRNG
        self.prng = random.Random(self.seed)

        # 2D grid where True = wall, False = empty
        self.grid = self._initialize_grid()

        # Apply smoothing steps
        for _ in range(self.smoothing_iterations):
            self.grid = self._apply_cellular_automata_smoothing()

        # Write results to the inherited `self.walls` set
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    self.add_wall(x, y)

    # [UTILITY METHODS]
    def _initialize_grid(self) -> list[list[bool]]:
        """
        Randomly fills the grid with walls based on the fill probability,
        ensuring edges are always walls to enclose the map.

        Returns:
            A 2D list of booleans representing the initial state.
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Always create walls on the map edges
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append(True)
                else:
                    # Deterministic random generation based on fill_probability
                    row.append(self.prng.random() < self.fill_probability)
            grid.append(row)
        return grid

    def _apply_cellular_automata_smoothing(self) -> list[list[bool]]:
        """
        Applies one iteration of cellular automata smoothing.
        Checks the 8 neighbors of each cell.
        If a cell has > 4 wall neighbors, it becomes a wall.
        If a cell has < 4 wall neighbors, it becomes empty space.

        Time Complexity: O(N) where N is width * height, because we do a constant
        amount of work (checking 8 neighbors) for each cell.

        Returns:
            The new 2D list of booleans after smoothing.
        """
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbor_wall_count = self._get_surrounding_wall_count(x, y)

                # Apply rules:
                if neighbor_wall_count > 4:
                    new_grid[y][x] = True
                elif neighbor_wall_count < 4:
                    new_grid[y][x] = False
                else:
                    # If exactly 4, keep current state
                    new_grid[y][x] = self.grid[y][x]

        return new_grid

    def _get_surrounding_wall_count(self, grid_x: int, grid_y: int) -> int:
        """
        Counts the number of wall neighbors in the 8 adjacent cells.
        Cells outside the map bounds are considered walls.

        Args:
            grid_x: X coordinate of the cell.
            grid_y: Y coordinate of the cell.

        Returns:
            Number of neighboring walls (0-8).
        """
        wall_count = 0
        for neighbor_y in range(grid_y - 1, grid_y + 2):
            for neighbor_x in range(grid_x - 1, grid_x + 2):
                if neighbor_x == grid_x and neighbor_y == grid_y:
                    continue

                # Out of bounds is considered a wall to encourage enclosed areas
                if neighbor_x < 0 or neighbor_x >= self.width or neighbor_y < 0 or neighbor_y >= self.height:
                    wall_count += 1
                elif self.grid[neighbor_y][neighbor_x]:
                    wall_count += 1

        return wall_count
