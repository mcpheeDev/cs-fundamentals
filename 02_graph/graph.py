class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self._adj = {}   # { node: { neighbour: weight } }

    def add_node(self, node):
        # TODO: add node to _adj if not already present
        pass

    def add_edge(self, u, v, weight=1):
        # TODO: add edge u→v with given weight
        # if not directed, also add v→u
        # auto-create nodes if they don't exist
        pass

    def remove_node(self, node):
        # TODO: remove node and all edges pointing to/from it
        # Raise KeyError if node not found
        pass

    def remove_edge(self, u, v):
        # TODO: remove edge u→v
        # Raise KeyError if edge not found
        pass

    def neighbours(self, node):
        # TODO: return list of nodes adjacent to node
        pass

    def has_edge(self, u, v):
        # TODO: return True if edge u→v exists
        pass

    def nodes(self):
        return list(self._adj.keys())

    def edges(self):
        # TODO: return list of (u, v, weight) tuples
        # for undirected graphs, don't return both (A,B) and (B,A)
        pass

    def bfs(self, start):
        # TODO: breadth-first traversal from start
        # return list of nodes in the order they were visited
        # use a queue (collections.deque)
        pass

    def dfs(self, start, visited=None):
        # TODO: depth-first traversal from start (recursive)
        # return list of nodes in the order they were visited
        pass

    def is_connected(self):
        # TODO: return True if every node is reachable from the first node
        pass

    def has_cycle(self):
        # TODO: return True if the graph contains at least one cycle
        # Hint: DFS colouring — WHITE (unvisited), GREY (in progress), BLACK (done)
        # A cycle exists if you reach a GREY node during DFS
        pass

    def display(self):
        kind = "Directed" if self.directed else "Undirected"
        print(f"{kind} graph — {len(self._adj)} nodes")
        for node in sorted(self._adj):
            nbrs = ", ".join(f"{v}({w})" for v, w in self._adj[node].items())
            print(f"  {node} → [{nbrs}]")
