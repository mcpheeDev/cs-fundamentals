from graph import Graph

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

def test_raises(name, fn, err):
    global passed, failed
    try:
        fn()
        print(f"  ✗  {name}  (no exception raised)")
        failed += 1
    except err:
        print(f"  ✓  {name}")
        passed += 1


print("\n── Undirected graph ──────────────────────────────────")
g = Graph(directed=False)
g.add_edge("A", "B", 4)
g.add_edge("A", "C", 2)
g.add_edge("B", "C", 5)
g.add_edge("C", "D", 3)

test_true("A→B exists", g.has_edge("A", "B"))
test_true("B→A exists (undirected)", g.has_edge("B", "A"))
test("neighbours of A", sorted(g.neighbours("A")), ["B", "C"])
test_true("is connected", g.is_connected())

g.remove_edge("A", "B")
test("after remove, A→B gone",  g.has_edge("A", "B"), False)
test("after remove, B→A gone",  g.has_edge("B", "A"), False)

test_raises("remove missing edge raises KeyError",
            lambda: g.remove_edge("A", "B"), KeyError)

print("\n── Directed graph ────────────────────────────────────")
d = Graph(directed=True)
d.add_edge("X", "Y", 1)
d.add_edge("Y", "Z", 1)
test_true("X→Y exists", d.has_edge("X", "Y"))
test("Y→X does not exist (directed)", d.has_edge("Y", "X"), False)

print("\n── BFS ───────────────────────────────────────────────")
g2 = Graph(directed=False)
for u, v in [("A","B"),("A","C"),("B","D"),("C","D"),("D","E")]:
    g2.add_edge(u, v)
bfs = g2.bfs("A")
test("BFS starts at A", bfs[0], "A")
test_true("BFS visits all 5 nodes", len(bfs) == 5)
# B and C must appear before D (they're closer to A)
test_true("BFS visits B before D", bfs.index("B") < bfs.index("D"))
test_true("BFS visits C before D", bfs.index("C") < bfs.index("D"))

print("\n── DFS ───────────────────────────────────────────────")
dfs = g2.dfs("A")
test("DFS starts at A", dfs[0], "A")
test_true("DFS visits all 5 nodes", len(dfs) == 5)

print("\n── Cycle detection ───────────────────────────────────")
no_cycle = Graph(directed=True)
no_cycle.add_edge("A", "B")
no_cycle.add_edge("B", "C")
test("no cycle in A→B→C", no_cycle.has_cycle(), False)

has_cycle = Graph(directed=True)
has_cycle.add_edge("A", "B")
has_cycle.add_edge("B", "C")
has_cycle.add_edge("C", "A")
test("cycle in A→B→C→A", has_cycle.has_cycle(), True)

print("\n── Remove node ───────────────────────────────────────")
g3 = Graph(directed=False)
g3.add_edge("A", "B")
g3.add_edge("B", "C")
g3.remove_node("B")
test("B removed from nodes", "B" in g3.nodes(), False)
test("A's neighbours no longer include B", "B" in g3.neighbours("A"), False)
test_raises("remove missing node raises KeyError",
            lambda: g3.remove_node("B"), KeyError)

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
