"""
pathfinding.py — Dijkstra's algorithm and A* search applied to a UK city
road network. Shows step-by-step tables matching the exact format used
in academic trace exercises.

Run:  python3 pathfinding.py
"""

import heapq
import math


# ── UK City Road Network ──────────────────────────────────────────────────────
# Edges: (city_a, city_b, distance_miles)

ROAD_NETWORK = [
    ("London",     "Oxford",       60),
    ("London",     "Cambridge",    60),
    ("London",     "Bristol",     120),
    ("Oxford",     "Birmingham",   65),
    ("Oxford",     "Bristol",      75),
    ("Cambridge",  "Birmingham",  100),
    ("Cambridge",  "Norwich",      60),
    ("Birmingham", "Manchester",   85),
    ("Birmingham", "Leeds",       120),
    ("Bristol",    "Cardiff",      45),
    ("Manchester", "Leeds",        45),
    ("Manchester", "Liverpool",    35),
    ("Leeds",      "York",         25),
    ("Leeds",      "Newcastle",   100),
    ("York",       "Newcastle",    80),
    ("Newcastle",  "Edinburgh",   105),
    ("Edinburgh",  "Glasgow",      45),
    ("Liverpool",  "Glasgow",     220),
]

# Approximate coordinates (lat, lon) for heuristic distance in A*
COORDS = {
    "London":     (51.5, -0.1),
    "Oxford":     (51.7, -1.25),
    "Cambridge":  (52.2,  0.12),
    "Bristol":    (51.45, -2.6),
    "Birmingham": (52.5,  -1.9),
    "Cardiff":    (51.5,  -3.2),
    "Norwich":    (52.6,   1.3),
    "Manchester": (53.5,  -2.2),
    "Liverpool":  (53.4,  -3.0),
    "Leeds":      (53.8,  -1.5),
    "York":       (53.96, -1.08),
    "Newcastle":  (54.97, -1.6),
    "Edinburgh":  (55.95, -3.2),
    "Glasgow":    (55.86, -4.25),
}


def build_graph(edges):
    graph = {}
    for a, b, w in edges:
        graph.setdefault(a, {})[b] = w
        graph.setdefault(b, {})[a] = w
    return graph


def haversine(city_a, city_b):
    """Straight-line distance (miles) between two cities — used as A* heuristic."""
    lat1, lon1 = COORDS[city_a]
    lat2, lon2 = COORDS[city_b]
    R = 3958.8   # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


# ── Dijkstra's Algorithm ──────────────────────────────────────────────────────

def dijkstra(graph, start, end, verbose=True):
    """
    Find the shortest path from start to end using Dijkstra's algorithm.
    Returns (distance, path, steps_table).
    """
    dist     = {node: float('inf') for node in graph}
    prev     = {node: None         for node in graph}
    visited  = set()
    dist[start] = 0
    pq = [(0, start)]
    steps = []

    if verbose:
        print(f"\n  Dijkstra's: {start} → {end}")
        print(f"  {'Node':<14} {'Dist':>6}  {'Prev':<14} {'Visited'}")
        print("  " + "─" * 48)

    while pq:
        current_dist, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        steps.append((node, dist[node], prev[node]))

        if verbose:
            print(f"  {node:<14} {dist[node]:>6}  {str(prev[node]):<14} ✓")

        if node == end:
            break

        for neighbour, weight in graph[node].items():
            if neighbour not in visited:
                new_dist = dist[node] + weight
                if new_dist < dist[neighbour]:
                    dist[neighbour] = new_dist
                    prev[neighbour] = node
                    heapq.heappush(pq, (new_dist, neighbour))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if verbose:
        print(f"\n  Shortest path: {' → '.join(path)}")
        print(f"  Total distance: {dist[end]} miles\n")

    return dist[end], path, steps


# ── A* Algorithm ─────────────────────────────────────────────────────────────

def astar(graph, start, end, verbose=True):
    """
    Find the shortest path using A* with haversine heuristic.
    f(n) = g(n) + h(n)  where g = cost so far, h = straight-line to goal.
    """
    g     = {node: float('inf') for node in graph}
    prev  = {node: None         for node in graph}
    g[start] = 0
    pq = [(haversine(start, end), start)]
    visited = set()
    steps = []

    if verbose:
        print(f"\n  A*: {start} → {end}")
        print(f"  {'Node':<14} {'g(n)':>6}  {'h(n)':>6}  {'f(n)':>6}  {'Visited'}")
        print("  " + "─" * 56)

    while pq:
        f, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        h = haversine(node, end)
        steps.append((node, g[node], h, g[node] + h))

        if verbose:
            print(f"  {node:<14} {g[node]:>6.0f}  {h:>6.0f}  {g[node]+h:>6.0f}  ✓")

        if node == end:
            break

        for neighbour, weight in graph[node].items():
            if neighbour not in visited:
                tentative_g = g[node] + weight
                if tentative_g < g[neighbour]:
                    g[neighbour] = tentative_g
                    prev[neighbour] = node
                    f_score = tentative_g + haversine(neighbour, end)
                    heapq.heappush(pq, (f_score, neighbour))

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if verbose:
        print(f"\n  Shortest path: {' → '.join(path)}")
        print(f"  Total distance: {g[end]:.0f} miles\n")

    return g[end], path, steps


# ── Comparison ────────────────────────────────────────────────────────────────

def compare(graph, routes):
    print("=" * 65)
    print("DIJKSTRA'S vs A*  —  NODE VISITS COMPARISON")
    print("=" * 65)
    print(f"  {'Route':<30} {'Dijkstra nodes':>15}  {'A* nodes':>10}  {'Same path?'}")
    print("  " + "─" * 62)
    for start, end in routes:
        _, dp, ds = dijkstra(graph, start, end, verbose=False)
        _, ap, as_ = astar(graph, start, end, verbose=False)
        same = "✓" if dp == ap else "✗"
        print(f"  {start+' → '+end:<30} {len(ds):>15}  {len(as_):>10}  {same}")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    graph = build_graph(ROAD_NETWORK)

    dijkstra(graph, "London", "Edinburgh")
    astar(graph,    "London", "Edinburgh")

    compare(graph, [
        ("London",     "Edinburgh"),
        ("Bristol",    "Newcastle"),
        ("Cardiff",    "Glasgow"),
        ("Norwich",    "Liverpool"),
        ("Cambridge",  "York"),
    ])
