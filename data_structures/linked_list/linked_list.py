"""
linked_list.py — Core doubly-linked list implementation.

Supports O(1) head/tail insertion, O(n) search, and full
forward/backward traversal. Used as the backbone for playlist.py
and browser_history.py.
"""


class Node:
    """A single node storing data and pointers to neighbours."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"Node({self.data!r})"


class DoublyLinkedList:
    """
    A doubly-linked list with O(1) head and tail operations.

    Attributes
    ----------
    head : Node | None   — first node
    tail : Node | None   — last node
    _size : int          — number of nodes (private)
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    # ── Properties ────────────────────────────────────────────────────────────

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __reversed__(self):
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def __contains__(self, data):
        return self.find(data) is not None

    def __repr__(self):
        items = " ⟷ ".join(repr(d) for d in self)
        return f"DLL[{items}]"

    def is_empty(self):
        return self._size == 0

    # ── Insertion ─────────────────────────────────────────────────────────────

    def append(self, data):
        """Add a node to the tail — O(1)."""
        node = Node(data)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, data):
        """Add a node to the head — O(1)."""
        node = Node(data)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def insert_after(self, target_data, new_data):
        """Insert new_data immediately after the first node containing target_data — O(n)."""
        node = self.find(target_data)
        if node is None:
            raise ValueError(f"{target_data!r} not found in list")
        new_node = Node(new_data)
        new_node.prev = node
        new_node.next = node.next
        if node.next:
            node.next.prev = new_node
        else:
            self.tail = new_node
        node.next = new_node
        self._size += 1

    def insert_before(self, target_data, new_data):
        """Insert new_data immediately before the first node containing target_data — O(n)."""
        node = self.find(target_data)
        if node is None:
            raise ValueError(f"{target_data!r} not found in list")
        new_node = Node(new_data)
        new_node.next = node
        new_node.prev = node.prev
        if node.prev:
            node.prev.next = new_node
        else:
            self.head = new_node
        node.prev = new_node
        self._size += 1

    # ── Removal ───────────────────────────────────────────────────────────────

    def remove(self, data):
        """Remove the first node containing data — O(n). Raises ValueError if not found."""
        node = self.find(data)
        if node is None:
            raise ValueError(f"{data!r} not found in list")
        self._unlink(node)

    def pop_head(self):
        """Remove and return the head's data — O(1)."""
        if self.is_empty():
            raise IndexError("pop from empty list")
        data = self.head.data
        self._unlink(self.head)
        return data

    def pop_tail(self):
        """Remove and return the tail's data — O(1)."""
        if self.is_empty():
            raise IndexError("pop from empty list")
        data = self.tail.data
        self._unlink(self.tail)
        return data

    def _unlink(self, node):
        """Detach a node from the list."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self._size -= 1

    # ── Search ────────────────────────────────────────────────────────────────

    def find(self, data):
        """Return the first Node containing data, or None — O(n)."""
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None

    def index_of(self, data):
        """Return the 0-based index of the first node containing data — O(n)."""
        for i, item in enumerate(self):
            if item == data:
                return i
        raise ValueError(f"{data!r} not found")

    # ── Display ───────────────────────────────────────────────────────────────

    def display(self):
        if self.is_empty():
            print("(empty list)")
            return
        items = list(self)
        print("HEAD ⟶ " + " ⟷ ".join(str(i) for i in items) + " ⟵ TAIL")
        print(f"       {len(self)} node(s)")


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    dll = DoublyLinkedList()

    print("=== Doubly Linked List Demo ===\n")

    for name in ["Alice", "Bob", "Carol", "Dave"]:
        dll.append(name)
    dll.display()

    print("\nPrepend 'Zara':")
    dll.prepend("Zara")
    dll.display()

    print("\nInsert 'Eve' after 'Bob':")
    dll.insert_after("Bob", "Eve")
    dll.display()

    print("\nRemove 'Carol':")
    dll.remove("Carol")
    dll.display()

    print("\nForward traversal:", list(dll))
    print("Backward traversal:", list(reversed(dll)))
    print(f"'Eve' in list: {'Eve' in dll}")
    print(f"Length: {len(dll)}")
