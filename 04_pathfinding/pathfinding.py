import heapq
import math

# ── City network ──────────────────────────────────────────────────────────────
# TODO: define at least 10 UK cities with road distances (miles)
# Format: list of (city_a, city_b, distance)

ROADS = [
    # e.g. ("London", "Oxford", 60),
    # TODO: fill this in
]

# TODO: define approximate (latitude, longitude) for each city
# Used by the A* heuristic to estimate straight-line distance
COORDS = {
    # e.g. "London": (51.5, -0.1),
    # TODO: fill this in
}


def build_graph(roads):
    """Convert a list of (city_a, city_b, distance) into an adjacency dict."""
    # TODO
    pass


def haversine(city_a, city_b):
    """
    Straight-line distance in miles between two cities using their coordinates.
    Used as the A* heuristic — it never overestimates (admissible).

    Formula:
      a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
      distance = 2 * R * arcsin(√a)    where R = 3958.8 miles
    """
    # TODO
    pass


def dijkstra(graph, start, end, verbose=True):
    """
    TODO: Dijkstra's shortest path algorithm.

    Steps:
      1. Set dist[start]=0, all others=infinity
      2. Push (0, start) to a min-heap
      3. While heap not empty:
           pop the lowest-cost node
           skip if already visited
           mark as visited
           for each neighbour:
             if dist[node] + edge_weight < dist[neighbour]:
               update dist[neighbour] and prev[neighbour]
               push to heap
      4. Reconstruct path from prev[]
      5. Return (total_distance, path_list)
    """
    pass


def astar(graph, start, end, verbose=True):
    """
    TODO: A* search algorithm.

    Same as Dijkstra's but the priority queue uses f(n) = g(n) + h(n)
    where h(n) = haversine(n, end).

    Return (total_distance, path_list).
    """
    pass


def compare(graph, routes):
    """
    TODO: run both algorithms on each (start, end) pair.
    Print a table showing nodes visited and whether paths match.
    """
    pass


if __name__ == "__main__":
    graph = build_graph(ROADS)

    # Test on a few routes
    dijkstra(graph, "London", "Edinburgh")
    astar(graph,    "London", "Edinburgh")
    compare(graph, [
        ("London",    "Edinburgh"),
        ("Bristol",   "Newcastle"),
        ("Cardiff",   "Glasgow"),
    ])
