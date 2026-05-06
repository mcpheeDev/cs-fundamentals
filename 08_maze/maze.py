import random
import time


class Maze:
    WALL  = "#"
    OPEN  = " "
    START = "S"
    END   = "E"
    PATH  = "·"
    DEAD  = "X"

    def __init__(self, rows=21, cols=41, seed=None):
        if seed is not None:
            random.seed(seed)
        # Ensure odd dimensions
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        # Fill everything with walls
        self.grid = [[self.WALL] * self.cols for _ in range(self.rows)]
        self.solution = []
        self._generate(1, 1)
        self.grid[1][1]                         = self.START
        self.grid[self.rows - 2][self.cols - 2] = self.END
        self.start = (1, 1)
        self.end   = (self.rows - 2, self.cols - 2)

    def _generate(self, row, col):
        """
        TODO: recursive backtracking maze generation.

        1. Mark (row, col) as OPEN
        2. Build a list of 4 directions as (dr, dc) with step size 2
           e.g. up=(−2,0), down=(+2,0), left=(0,−2), right=(0,+2)
        3. Shuffle the directions
        4. For each direction:
             - Calculate the neighbour (row+dr, col+dc)
             - Check it's within bounds and still a WALL
             - If so: knock down the wall between current and neighbour
               (set grid[row+dr//2][col+dc//2] = OPEN)
             - Recurse into the neighbour
        """
        pass

    def solve(self, row=None, col=None, path=None):
        """
        TODO: recursive DFS solver.

        Returns True if the end is reached, False if this is a dead end.

        Steps:
          - Default row, col to self.start; path to []
          - Return False if out of bounds, WALL, or DEAD
          - Return False if already marked PATH (cycle prevention)
          - Mark cell as PATH, add to path list
          - If we've reached self.end, save path and return True
          - Try all 4 directions recursively
          - If none succeed, backtrack:
              remove from path, mark cell as DEAD, return False
        """
        pass

    def display(self, colour=True):
        """
        TODO: print the maze. Use double-width chars for walls.
        Optionally use ANSI colour codes.
        """
        pass

    def stats(self):
        print(f"  Size:      {self.rows} × {self.cols}")
        print(f"  Solution:  {len(self.solution)} steps")


if __name__ == "__main__":
    print("Generating maze...")
    maze = Maze(rows=21, cols=41, seed=42)
    print("Unsolved:")
    maze.display()

    print("Solving...")
    t = time.perf_counter()
    solved = maze.solve()
    elapsed = (time.perf_counter() - t) * 1000

    if solved:
        print("Solved:")
        maze.display()
        maze.stats()
        print(f"  Solve time: {elapsed:.2f}ms")
    else:
        print("No solution found.")
