"""
maze_solver.py — Generate a random maze using recursive backtracking,
then solve it using recursive DFS with backtracking.

Displays the maze in ASCII with the solution path highlighted.

Run:  python3 maze_solver.py
"""

import random
import time


class Maze:
    """
    A maze generated and solved entirely through recursion.

    Generation: recursive backtracking (perfect maze — exactly one path
                between any two cells).
    Solving:    recursive DFS with backtracking — marks dead ends and
                traces the solution path.

    Cell states:
        '#'  wall
        ' '  open passage
        'S'  start
        'E'  end
        '·'  solution path
        'X'  explored / dead end
    """

    WALL = "#"
    OPEN = " "
    START = "S"
    END   = "E"
    PATH  = "·"
    DEAD  = "X"

    def __init__(self, rows=15, cols=31):
        # Dimensions must be odd for the grid structure to work correctly
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.grid = [[self.WALL] * self.cols for _ in range(self.rows)]
        self._generate(1, 1)
        self.grid[1][1]                         = self.START
        self.grid[self.rows - 2][self.cols - 2] = self.END
        self.start = (1, 1)
        self.end   = (self.rows - 2, self.cols - 2)
        self.solution = []

    # ── Generation (recursive backtracking) ───────────────────────────────────

    def _generate(self, row, col):
        """Carve passages from (row, col) by visiting random unvisited neighbours."""
        self.grid[row][col] = self.OPEN
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                if self.grid[nr][nc] == self.WALL:
                    # Knock down the wall between current and neighbour
                    self.grid[row + dr // 2][col + dc // 2] = self.OPEN
                    self._generate(nr, nc)   # ← recursion

    # ── Solving (recursive DFS with backtracking) ─────────────────────────────

    def solve(self, row=None, col=None, path=None):
        """
        Recursively explore the maze from (row, col).
        Returns True when the end is reached, False on dead ends.
        """
        if row is None:
            row, col = self.start
            path = []

        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if self.grid[row][col] in (self.WALL, self.DEAD):
            return False
        if self.grid[row][col] == self.PATH:
            return False   # already visited

        # Mark as part of current path
        if self.grid[row][col] == self.OPEN:
            self.grid[row][col] = self.PATH
        path.append((row, col))

        if (row, col) == self.end or self.grid[row][col] == self.END:
            self.solution = path[:]
            return True

        # Try all four directions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.solve(row + dr, col + dc, path):
                return True

        # Backtrack — this path is a dead end
        path.pop()
        if self.grid[row][col] == self.PATH:
            self.grid[row][col] = self.DEAD
        return False

    # ── Display ───────────────────────────────────────────────────────────────

    COLOURS = {
        "#": "\033[90m",    # grey  — wall
        " ": "\033[0m",     # reset — open
        "S": "\033[92m",    # green — start
        "E": "\033[91m",    # red   — end
        "·": "\033[93m",    # yellow — solution path
        "X": "\033[34m",    # blue  — dead end explored
    }
    RESET = "\033[0m"

    def display(self, colour=True):
        print()
        for row in self.grid:
            line = ""
            for cell in row:
                char = {
                    self.WALL:  "██",
                    self.OPEN:  "  ",
                    self.START: "S ",
                    self.END:   "E ",
                    self.PATH:  "· ",
                    self.DEAD:  "  ",
                }.get(cell, "  ")
                if colour:
                    line += self.COLOURS.get(cell, "") + char + self.RESET
                else:
                    line += char
            print(line)
        print()

    def stats(self):
        total_open  = sum(row.count(self.OPEN)  +
                         row.count(self.PATH)   +
                         row.count(self.DEAD)
                         for row in self.grid)
        print(f"  Maze size:       {self.rows} × {self.cols}")
        print(f"  Solution length: {len(self.solution)} steps")
        print(f"  Open cells:      {total_open}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    random.seed(42)

    print("Generating maze...")
    maze = Maze(rows=21, cols=41)
    print("Unsolved maze:")
    maze.display()

    print("Solving...")
    t = time.perf_counter()
    success = maze.solve()
    elapsed = (time.perf_counter() - t) * 1000

    if success:
        print("Solved maze (yellow = solution path, blue = dead ends explored):")
        maze.display()
        maze.stats()
        print(f"  Solve time:      {elapsed:.2f}ms")
    else:
        print("No solution found.")
