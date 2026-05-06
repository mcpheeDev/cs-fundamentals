from maze import Maze

passed = 0
failed = 0

def test(name, got, expected):
    global passed, failed
    if got == expected:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  {name}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")
        failed += 1

def test_true(name, condition):
    test(name, condition, True)


print("\n── Generation ────────────────────────────────────────")
m = Maze(rows=11, cols=11, seed=1)
test("rows set correctly", m.rows, 11)
test("cols set correctly", m.cols, 11)
test("start cell is S", m.grid[1][1], "S")
test("end cell is E",   m.grid[m.rows-2][m.cols-2], "E")

# Corners should be walls
test("top-left is wall",     m.grid[0][0], "#")
test("top-right is wall",    m.grid[0][m.cols-1], "#")
test("bottom-left is wall",  m.grid[m.rows-1][0], "#")
test("bottom-right is wall", m.grid[m.rows-1][m.cols-1], "#")

# Grid should have some open cells
open_cells = sum(row.count(" ") + row.count("S") + row.count("E")
                 for row in m.grid)
test_true("maze has open cells", open_cells > 0)

print("\n── Even dimensions auto-corrected ────────────────────")
m2 = Maze(rows=10, cols=10, seed=1)
test_true("even rows corrected to odd", m2.rows % 2 == 1)
test_true("even cols corrected to odd", m2.cols % 2 == 1)

print("\n── Solving ───────────────────────────────────────────")
m3 = Maze(rows=15, cols=15, seed=42)
result = m3.solve()
test("solve returns True (solution exists)", result, True)
test_true("solution is non-empty", len(m3.solution) > 0)
test("solution starts at start", m3.solution[0],  m3.start)
test("solution ends at end",     m3.solution[-1], m3.end)

# Solution path should be contiguous (each step is 1 cell away)
for i in range(len(m3.solution) - 1):
    r1, c1 = m3.solution[i]
    r2, c2 = m3.solution[i+1]
    dist = abs(r2-r1) + abs(c2-c1)
    test_true(f"solution step {i} is adjacent", dist == 1)

print("\n── Multiple mazes are different ──────────────────────")
import random
m4 = Maze(rows=11, cols=11, seed=1)
m5 = Maze(rows=11, cols=11, seed=99)
grids_differ = any(
    m4.grid[r][c] != m5.grid[r][c]
    for r in range(m4.rows) for c in range(m4.cols)
)
test_true("different seeds produce different mazes", grids_differ)

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
