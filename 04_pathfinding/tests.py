from pathfinding import build_graph, dijkstra, astar, ROADS, COORDS, haversine

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


print("\n── Setup ─────────────────────────────────────────────")
test_true("at least 10 cities defined", len(COORDS) >= 10)
test_true("at least 10 roads defined",  len(ROADS)  >= 10)

graph = build_graph(ROADS)

print("\n── build_graph ───────────────────────────────────────")
test_true("returns a dict", isinstance(graph, dict))
test_true("all cities in graph", all(c in graph for c in COORDS))
# Undirected: if A→B exists, B→A should too
a, b, _ = ROADS[0]
test_true("graph is undirected (A→B and B→A)",
          b in graph.get(a, {}) and a in graph.get(b, {}))

print("\n── haversine ─────────────────────────────────────────")
if "London" in COORDS and "Edinburgh" in COORDS:
    dist = haversine("London", "Edinburgh")
    test_true("London→Edinburgh haversine is a number", isinstance(dist, float))
    test_true("London→Edinburgh > 300 miles (straight line)", dist > 300)
    test_true("London→Edinburgh < 500 miles", dist < 500)
    test("haversine is symmetric", round(haversine("London","Edinburgh"),2),
                                    round(haversine("Edinburgh","London"),2))

print("\n── Dijkstra ──────────────────────────────────────────")
cities = list(COORDS.keys())
start, end = cities[0], cities[-1]
result = dijkstra(graph, start, end, verbose=False)
test_true("dijkstra returns a tuple", isinstance(result, tuple))
dist_d, path_d = result
test_true("path starts at start", path_d[0] == start)
test_true("path ends at end",     path_d[-1] == end)
test_true("distance is positive", dist_d > 0)

# Verify path is valid (each step is an actual edge)
for i in range(len(path_d) - 1):
    u, v = path_d[i], path_d[i+1]
    test_true(f"edge {u}→{v} exists in graph", v in graph.get(u, {}))

print("\n── A* ────────────────────────────────────────────────")
result_a = astar(graph, start, end, verbose=False)
test_true("astar returns a tuple", isinstance(result_a, tuple))
dist_a, path_a = result_a
test_true("astar path starts at start", path_a[0] == start)
test_true("astar path ends at end",     path_a[-1] == end)
test("dijkstra and astar find same distance",
     round(dist_d, 2), round(dist_a, 2))

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
