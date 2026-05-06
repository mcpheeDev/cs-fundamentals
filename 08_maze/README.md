# 08 – Maze Generator & Solver

## What you're building
Generate a random maze using recursive backtracking, then solve it
using recursive DFS. Display everything in ASCII.

## Part 1 — Generator (`maze.py`)
Use recursive backtracking to carve a perfect maze (exactly one path
between any two cells):

1. Start at cell (1, 1), mark it visited
2. Pick a random unvisited neighbour that is 2 steps away
3. Knock down the wall between current cell and that neighbour
4. Recurse into the neighbour
5. If no unvisited neighbours, backtrack

The grid should use `#` for walls and ` ` for passages.
Dimensions must be odd (e.g. 21×41) for the structure to work correctly.

## Part 2 — Solver (`maze.py`)
Solve the maze using recursive DFS with backtracking:

1. Start at the top-left open cell
2. Try moving in each direction
3. If you reach the end cell, you're done — record the path
4. If you hit a wall or already-visited cell, backtrack
5. Mark the solution path with `·` and dead ends with `X`

## Part 3 — Display
Render the maze in ASCII using double-width characters for walls
so it looks like a proper grid. Use colour escape codes if you want
(yellow for solution path, grey for dead ends).

Print stats after solving:
- Maze dimensions
- Number of solution steps
- Solve time in ms

## Run tests
```bash
python3 tests.py
```
