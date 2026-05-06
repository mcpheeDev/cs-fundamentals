"""
browser_history.py — Browser back/forward history using a doubly-linked list.

Mirrors how real browsers maintain navigation history: visiting a new page
truncates any forward history, while back/forward move the current pointer.

Run:  python3 browser_history.py
"""

from linked_list import DoublyLinkedList
from datetime import datetime


class Page:
    def __init__(self, url, title=None):
        self.url = url
        self.title = title or url
        self.visited_at = datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        return f"{self.title}  ({self.url})  [{self.visited_at}]"

    def __repr__(self):
        return f"Page({self.url!r})"

    def __eq__(self, other):
        return isinstance(other, Page) and self.url == other.url


class BrowserHistory:
    """
    Simulates browser history using a doubly-linked list.

    The _current pointer moves back/forward through the list.
    Visiting a new URL truncates everything forward of _current.
    """

    def __init__(self, home="https://www.google.com"):
        self._history = DoublyLinkedList()
        self._current = None
        self.visit(home, "Google")

    def visit(self, url, title=None):
        """Navigate to a new URL, discarding any forward history."""
        # Truncate forward history
        if self._current and self._current.next:
            node = self._current.next
            while node:
                nxt = node.next
                self._history._unlink(node)
                node = nxt

        page = Page(url, title)
        self._history.append(page)
        self._current = self._history.tail
        print(f"  🌐  Navigated to: {page.title}")

    def back(self):
        """Go back one page."""
        if self._current and self._current.prev:
            self._current = self._current.prev
            print(f"  ◀  Back: {self._current.data.title}")
            return self._current.data
        print("  ⚠  No previous page.")
        return None

    def forward(self):
        """Go forward one page."""
        if self._current and self._current.next:
            self._current = self._current.next
            print(f"  ▶  Forward: {self._current.data.title}")
            return self._current.data
        print("  ⚠  No forward page.")
        return None

    def current_page(self):
        return self._current.data if self._current else None

    def display(self):
        print(f"\n{'─'*55}")
        print(f"  Browser History  ({len(self._history)} page(s))")
        print(f"{'─'*55}")
        for page in self._history:
            marker = "► " if page == self.current_page() else "  "
            print(f"  {marker}{page}")
        print(f"{'─'*55}\n")


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Browser History Demo ===\n")

    browser = BrowserHistory()
    browser.visit("https://github.com", "GitHub")
    browser.visit("https://github.com/trending", "Trending — GitHub")
    browser.visit("https://github.com/python", "Python — GitHub")
    browser.display()

    print("Going back twice:")
    browser.back()
    browser.back()
    browser.display()

    print("Going forward once:")
    browser.forward()
    browser.display()

    print("Visiting a new page (forward history should be cleared):")
    browser.visit("https://docs.python.org", "Python Docs")
    browser.display()

    print("Trying to go forward (should fail — forward history cleared):")
    browser.forward()
