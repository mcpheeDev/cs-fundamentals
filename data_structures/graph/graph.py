"""
graph.py — Weighted directed/undirected graph implementation.

Backed by an adjacency list (dict of dicts). Supports BFS, DFS,
cycle detection, and degree queries. Used by social_network.py
and route_planner.py.

Run:  python3 graph.py
"""

from collections import deque


class Graph:
    """
    A weighted graph supporting both directed and undirected edges.

    Internally represented as:
        { node: { neighbour: weight, ... }, ... }
    """

    def __init__(self, directed=False):
        self.directed = directed
        self._adj = {}          # adjacency list
        self._node_data = {}    # optional metadata per node

    # ── Node operations ───────────────────────────────────────────────────────

    def add_node(self, node, **kwargs):
        """Add a node with optional metadata (e.g. add_node('A', label='Start'))."""
        if node not in self._adj:
            self._adj[node] = {}
        self._node_data[node] = kwargs

    def remove_node(self, node):
        """Remove a node and all its edges."""
        if node not in self._adj:
            raise KeyError(f"Node {node!r} not found")
        del self._adj[node]
        self._node_data.pop(node, None)
        for neighbours in self._adj.values():
            neighbours.pop(node, None)

    def nodes(self):
        return list(self._adj.keys())

    # ── Edge operations ───────────────────────────────────────────────────────

    def add_edge(self, u, v, weight=1):
        """Add a weighted edge from u to v (and v to u if undirected)."""
        for node in (u, v):
            if node not in self._adj:
                self.add_node(node)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight

    def remove_edge(self, u, v):
        """Remove the edge from u to v."""
        if v in self._adj.get(u, {}):
            del self._adj[u][v]
            if not self.directed:
                del self._adj[v][u]
        else:
            raise KeyError(f"Edge {u!r} → {v!r} not found")

    def has_edge(self, u, v):
        return v in self._adj.get(u, {})

    def weight(self, u, v):
        return self._adj[u][v]

    def edges(self):
        """Return all edges as (u, v, weight) tuples."""
        seen = set()
        result = []
        for u, neighbours in self._adj.items():
            for v, w in neighbours.items():
                key = (min(u, v), max(u, v)) if not self.directed else (u, v)
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def neighbours(self, node):
        return list(self._adj.get(node, {}).keys())

    def degree(self, node):
        """In-degree + out-degree for directed; just degree for undirected."""
        if self.directed:
            out_deg = len(self._adj.get(node, {}))
            in_deg  = sum(1 for nbrs in self._adj.values() if node in nbrs)
            return {"in": in_deg, "out": out_deg}
        return len(self._adj.get(node, {}))

    # ── Traversal ─────────────────────────────────────────────────────────────

    def bfs(self, start, verbose=True):
        """
        Breadth-first search from start.
        Returns nodes in the order visited.
        """
        if start not in self._adj:
            raise KeyError(f"{start!r} not in graph")
        visited = set()
        queue   = deque([start])
        order   = []
        visited.add(start)

        while queue:
            node = queue.popleft()
            order.append(node)
            if verbose:
                print(f"  Visit: {node}  |  queue: {list(queue)}")
            for neighbour in sorted(self._adj[node]):   # sorted for determinism
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return order

    def dfs(self, start, visited=None, verbose=True):
        """
        Depth-first search from start (recursive).
        Returns nodes in the order visited.
        """
        if visited is None:
            visited = set()
            if verbose:
                print(f"  DFS from {start}:")
        visited.add(start)
        order = [start]
        if verbose:
            print(f"  Visit: {start}")
        for neighbour in sorted(self._adj.get(start, {})):
            if neighbour not in visited:
                order.extend(self.dfs(neighbour, visited, verbose))
        return order

    def has_cycle(self):
        """Detect a cycle using DFS colouring (WHITE/GREY/BLACK)."""
        WHITE, GREY, BLACK = 0, 1, 2
        colour = {n: WHITE for n in self._adj}

        def dfs_cycle(node):
            colour[node] = GREY
            for nbr in self._adj[node]:
                if colour[nbr] == GREY:
                    return True
                if colour[nbr] == WHITE and dfs_cycle(nbr):
                    return True
            colour[node] = BLACK
            return False

        return any(dfs_cycle(n) for n in self._adj if colour[n] == WHITE)

    def is_connected(self):
        """Return True if all nodes are reachable from the first node."""
        if not self._adj:
            return True
        start = next(iter(self._adj))
        return len(self.bfs(start, verbose=False)) == len(self._adj)

    # ── Display ───────────────────────────────────────────────────────────────

    def display(self):
        kind = "Directed" if self.directed else "Undirected"
        print(f"\n{kind} Graph  ({len(self._adj)} nodes, {len(self.edges())} edges)")
        print("─" * 40)
        for node in sorted(self._adj):
            nbrs = self._adj[node]
            edges_str = ", ".join(f"{v}({w})" for v, w in sorted(nbrs.items()))
            print(f"  {node} → [{edges_str}]")
        print()


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Undirected Weighted Graph Demo ===")
    g = Graph(directed=False)
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 5),
        ("B", "D", 10), ("C", "D", 3), ("C", "E", 8), ("D", "E", 2),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    g.display()

    print("BFS from A:")
    g.bfs("A")

    print("\nDFS from A:")
    g.dfs("A")

    print(f"\nConnected: {g.is_connected()}")
    print(f"Has cycle: {g.has_cycle()}")
    print(f"Degree of C: {g.degree('C')}")
