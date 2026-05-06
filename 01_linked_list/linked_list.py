class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head  = None
        self.tail  = None
        self._size = 0

    def __len__(self):
        # TODO: return the number of nodes
        pass

    def __iter__(self):
        # TODO: yield each node's data from head to tail
        pass

    def __contains__(self, data):
        return self.find(data) is not None

    def is_empty(self):
        return self._size == 0

    def append(self, data):
        # TODO: create a new node and add it to the tail
        # Remember to handle the case where the list is empty
        pass

    def prepend(self, data):
        # TODO: create a new node and add it to the head
        pass

    def insert_after(self, target_data, new_data):
        # TODO: find the node containing target_data
        # then insert a new node immediately after it
        # Raise ValueError if target_data is not found
        pass

    def remove(self, data):
        # TODO: find and remove the first node containing data
        # Raise ValueError if not found
        # Hint: you'll need to update the prev/next pointers
        # of the surrounding nodes
        pass

    def find(self, data):
        # TODO: traverse from head, return the Node containing
        # data, or None if not found
        pass

    def display(self):
        # TODO: print in the format:
        # HEAD → A ↔ B ↔ C → TAIL
        # or "(empty)" if the list is empty
        pass


# ── Playlist ──────────────────────────────────────────────────────────────────

class Track:
    def __init__(self, title, artist, duration_secs):
        # TODO: store title, artist, duration_secs
        pass

    def __str__(self):
        # TODO: return "Title — Artist [m:ss]"
        pass

    def __eq__(self, other):
        # TODO: two tracks are equal if title AND artist match
        pass


class Playlist:
    def __init__(self, name):
        self.name     = name
        self._tracks  = DoublyLinkedList()
        self._current = None   # this will be a Node

    def add(self, track):
        # TODO: append track to the list
        # if _current is None, set it to the head node
        pass

    def add_next(self, track):
        # TODO: insert track immediately after the current node
        pass

    def remove(self, track):
        # TODO: remove the track from the list
        # if it's the current track, move current to next or prev
        pass

    def next_track(self):
        # TODO: advance _current to the next node
        # return the new current track, or None if at end
        pass

    def previous_track(self):
        # TODO: move _current back one node
        # return the new current track, or None if at start
        pass

    def shuffle(self):
        # TODO: collect all tracks into a list, shuffle it,
        # rebuild the linked list, reset _current to head
        import random
        pass

    def display(self):
        # TODO: print each track numbered, with ▶ marking the current one
        pass


# ── Browser History ───────────────────────────────────────────────────────────

class BrowserHistory:
    def __init__(self, home="https://google.com"):
        self._history = DoublyLinkedList()
        self._current = None
        self.visit(home)

    def visit(self, url):
        # TODO: add url to the list
        # IMPORTANT: truncate (delete) any nodes after _current first
        # then append the new url and move _current to it
        pass

    def back(self):
        # TODO: move _current to the previous node
        # return the url, or None if already at start
        pass

    def forward(self):
        # TODO: move _current to the next node
        # return the url, or None if already at end
        pass

    def current_page(self):
        return self._current.data if self._current else None

    def display(self):
        # TODO: print all urls, marking current with ►
        pass
