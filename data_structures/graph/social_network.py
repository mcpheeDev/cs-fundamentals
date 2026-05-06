"""
social_network.py — A social network modelled as a directed graph.

Demonstrates: graph traversal (BFS/DFS), degree analysis,
shortest connection paths, and friend recommendations.

Run:  python3 social_network.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from graph import Graph


class SocialNetwork:
    """
    A directed social network where an edge A → B means A follows B.
    Mutual edges indicate friendship.
    """

    def __init__(self, name):
        self.name  = name
        self._graph = Graph(directed=True)

    def add_user(self, username, **profile):
        self._graph.add_node(username, **profile)

    def follow(self, follower, followed):
        """follower follows followed (directed edge)."""
        self._graph.add_edge(follower, followed, weight=1)

    def unfollow(self, follower, followed):
        self._graph.remove_edge(follower, followed)

    def are_friends(self, a, b):
        """Friends = mutual follows."""
        return self._graph.has_edge(a, b) and self._graph.has_edge(b, a)

    def followers_of(self, user):
        """Who follows user (in-edges in directed graph)."""
        return [u for u in self._graph.nodes()
                if self._graph.has_edge(u, user)]

    def following(self, user):
        """Who does user follow (out-edges)."""
        return self._graph.neighbours(user)

    def friends_of(self, user):
        return [u for u in self.following(user) if self.are_friends(user, u)]

    def mutual_friends(self, a, b):
        return set(self.friends_of(a)) & set(self.friends_of(b))

    def degrees_of_separation(self, a, b):
        """BFS to find the shortest follow-path from a to b."""
        if a == b:
            return 0, [a]
        visited = {a}
        queue   = [(a, [a])]
        while queue:
            node, path = queue.pop(0)
            for neighbour in self._graph.neighbours(node):
                if neighbour == b:
                    return len(path), path + [b]
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [neighbour]))
        return -1, []   # not reachable

    def recommend_follows(self, user, top_n=3):
        """
        Recommend users to follow based on friends-of-friends.
        Excludes users already followed or the user themselves.
        """
        already_following = set(self.following(user)) | {user}
        scores = {}
        for friend in self.following(user):
            for fof in self.following(friend):
                if fof not in already_following:
                    scores[fof] = scores.get(fof, 0) + 1
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        return ranked[:top_n]

    def most_followed(self, top_n=5):
        """Return users ranked by follower count."""
        counts = {u: len(self.followers_of(u)) for u in self._graph.nodes()}
        return sorted(counts.items(), key=lambda x: -x[1])[:top_n]

    def display_profile(self, user):
        following  = self.following(user)
        followers  = self.followers_of(user)
        friends    = self.friends_of(user)
        print(f"\n  @{user}")
        print(f"  Following:  {len(following):>4}   {following[:5]}")
        print(f"  Followers:  {len(followers):>4}   {followers[:5]}")
        print(f"  Friends:    {len(friends):>4}   {friends[:5]}")


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sn = SocialNetwork("PyBook")

    users = ["alice", "bob", "carol", "dave", "eve",
             "frank", "grace", "henry"]
    for u in users:
        sn.add_user(u)

    # Build connections
    follows = [
        ("alice", "bob"), ("alice", "carol"), ("alice", "dave"),
        ("bob",   "alice"), ("bob",   "carol"), ("bob",   "eve"),
        ("carol", "alice"), ("carol", "dave"),  ("carol", "frank"),
        ("dave",  "eve"),   ("dave",  "frank"),
        ("eve",   "alice"), ("eve",   "bob"),   ("eve",   "grace"),
        ("frank", "carol"), ("frank", "grace"), ("frank", "henry"),
        ("grace", "henry"), ("grace", "eve"),
        ("henry", "frank"),
    ]
    for a, b in follows:
        sn.follow(a, b)

    print("=" * 50)
    print(f"  {sn.name} Social Network")
    print("=" * 50)

    # Profile
    sn.display_profile("alice")
    sn.display_profile("frank")

    # Friendship check
    print(f"\n  alice & bob friends? {sn.are_friends('alice', 'bob')}")
    print(f"  alice & dave friends? {sn.are_friends('alice', 'dave')}")

    # Mutual friends
    mutual = sn.mutual_friends("alice", "bob")
    print(f"  Mutual friends (alice, bob): {mutual}")

    # Degrees of separation
    print("\n  Degrees of separation:")
    for a, b in [("alice", "henry"), ("henry", "alice"), ("grace", "bob")]:
        deg, path = sn.degrees_of_separation(a, b)
        print(f"    {a} → {b}: {deg} steps   path: {' → '.join(path)}")

    # Recommendations
    print("\n  Recommended follows for alice:")
    for user, score in sn.recommend_follows("alice"):
        print(f"    @{user}  (mutual connections: {score})")

    # Most followed
    print("\n  Most followed users:")
    for user, count in sn.most_followed():
        bar = "█" * count
        print(f"    @{user:<8} {bar} {count}")
