# 04 – Pathfinding

## What you're building
Dijkstra's algorithm and A*, applied to a real city road network.

## Part 1 — Dijkstra's Algorithm (`pathfinding.py`)
Given a weighted graph, find the shortest path between two nodes.

- Use a priority queue (heapq) to always expand the cheapest node next
- Track `dist[node]` (shortest known distance from start)
- Track `prev[node]` (which node we came from)
- Reconstruct the path at the end by walking back through `prev`
- Print a step-by-step table: Node | Distance | Previous | Visited

## Part 2 — A* Algorithm (`pathfinding.py`)
Like Dijkstra's but uses a heuristic to guide the search toward the goal.

- f(n) = g(n) + h(n)
  - g(n) = actual cost from start to n
  - h(n) = estimated cost from n to goal (your heuristic)
- For the city network, use straight-line (haversine) distance as h(n)
- Print a step-by-step table: Node | g(n) | h(n) | f(n) | Visited

## Part 3 — City Network (`pathfinding.py`)
Define a UK city road network (at least 10 cities, realistic distances).
Include approximate lat/lon coordinates for each city for the heuristic.

Run both algorithms on several routes and compare:
- Number of nodes visited
- Whether they find the same path
- When A* visits fewer nodes (and why)

## Run tests
```bash
python3 tests.py
```
