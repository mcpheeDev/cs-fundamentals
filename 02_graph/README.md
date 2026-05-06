# 02 – Graph

## What you're building
A weighted graph data structure, then two applications on top of it.

## Part 1 — The Graph (`graph.py`)
Implement an adjacency-list graph supporting both directed and undirected edges.

Methods to implement:
- `add_node(node)` — add a node
- `add_edge(u, v, weight=1)` — add a weighted edge (bidirectional if undirected)
- `remove_node(node)` — remove a node and all its edges
- `remove_edge(u, v)` — remove a specific edge
- `neighbours(node)` — return list of adjacent nodes
- `has_edge(u, v)` — True/False
- `bfs(start)` — breadth-first search, return nodes in visit order
- `dfs(start)` — depth-first search (recursive), return nodes in visit order
- `is_connected()` — True if all nodes reachable from the first node
- `has_cycle()` — True if the graph contains a cycle

## Part 2 — Social Network (`social_network.py`)
A directed follower network built on your graph where A→B means A follows B.

- `follow(a, b)` / `unfollow(a, b)`
- `are_friends(a, b)` — True if they follow each other
- `mutual_friends(a, b)` — set of common friends
- `degrees_of_separation(a, b)` — BFS shortest follow-path, return (steps, path)
- `recommend_follows(user)` — suggest users based on friends-of-friends

## Part 3 — Route Planner (`route_planner.py`)
Apply your graph to a real UK city road network (you define the edges).
- Find shortest driving route between any two cities
- Display the route and total distance

## Run tests
```bash
python3 tests.py
```
