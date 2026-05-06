"""
playlist.py — A music playlist manager built on a doubly-linked list.

Supports shuffle-free ordered playback, queue/dequeue tracks, and
an interactive CLI to manage your queue.

Run:  python3 playlist.py
"""

from linked_list import DoublyLinkedList
import random
import time


class Track:
    """Represents a single music track."""

    def __init__(self, title, artist, duration_secs):
        self.title = title
        self.artist = artist
        self.duration_secs = duration_secs

    @property
    def duration_str(self):
        m, s = divmod(self.duration_secs, 60)
        return f"{m}:{s:02d}"

    def __str__(self):
        return f"♪  {self.title} — {self.artist}  [{self.duration_str}]"

    def __repr__(self):
        return f"Track({self.title!r}, {self.artist!r})"

    def __eq__(self, other):
        return isinstance(other, Track) and self.title == other.title and self.artist == other.artist


class Playlist:
    """
    An ordered music playlist backed by a DoublyLinkedList.

    Allows O(1) next/previous track navigation and O(1) add-to-end.
    """

    def __init__(self, name):
        self.name = name
        self._tracks = DoublyLinkedList()
        self._current = None       # current Node being played

    # ── Track management ──────────────────────────────────────────────────────

    def add(self, track):
        """Append a track to the end of the playlist."""
        self._tracks.append(track)
        if self._current is None:
            self._current = self._tracks.head

    def add_next(self, track):
        """Queue a track to play immediately after the current one."""
        if self._current is None:
            self.add(track)
        else:
            self._tracks.insert_after(self._current.data, track)

    def remove(self, track):
        """Remove a track from the playlist."""
        if self._current and self._current.data == track:
            self._current = self._current.next or self._current.prev
        self._tracks.remove(track)

    def shuffle(self):
        """Randomly reorder tracks (Fisher-Yates on a list, then rebuild)."""
        items = list(self._tracks)
        random.shuffle(items)
        self._tracks = DoublyLinkedList()
        for t in items:
            self._tracks.append(t)
        self._current = self._tracks.head
        print("🔀  Playlist shuffled.")

    # ── Playback ──────────────────────────────────────────────────────────────

    @property
    def now_playing(self):
        return self._current.data if self._current else None

    def next_track(self):
        """Advance to the next track."""
        if self._current and self._current.next:
            self._current = self._current.next
            return self._current.data
        return None

    def previous_track(self):
        """Go back to the previous track."""
        if self._current and self._current.prev:
            self._current = self._current.prev
            return self._current.data
        return None

    # ── Display ───────────────────────────────────────────────────────────────

    def total_duration(self):
        secs = sum(t.duration_secs for t in self._tracks)
        h, rem = divmod(secs, 3600)
        m, s = divmod(rem, 60)
        return f"{h}h {m}m {s}s" if h else f"{m}m {s}s"

    def display(self):
        print(f"\n{'═'*50}")
        print(f"  📀  {self.name}   ({len(self._tracks)} tracks · {self.total_duration()})")
        print(f"{'═'*50}")
        for i, track in enumerate(self._tracks, 1):
            marker = "▶ " if track == self.now_playing else "  "
            print(f"  {marker}{i:>2}. {track}")
        print(f"{'═'*50}\n")


# ── Interactive CLI ───────────────────────────────────────────────────────────

SEED_TRACKS = [
    Track("Blinding Lights",   "The Weeknd",    200),
    Track("Levitating",        "Dua Lipa",      203),
    Track("Stay",              "The Kid LAROI",  141),
    Track("Peaches",           "Justin Bieber",  198),
    Track("Good 4 U",          "Olivia Rodrigo", 178),
    Track("Montero",           "Lil Nas X",      137),
    Track("Bad Habits",        "Ed Sheeran",     231),
    Track("Heat Waves",        "Glass Animals",  238),
]

def run_cli():
    pl = Playlist("My Playlist")
    for t in SEED_TRACKS:
        pl.add(t)

    commands = {
        "l": ("list",     "display the playlist"),
        "n": ("next",     "skip to next track"),
        "p": ("prev",     "go to previous track"),
        "a": ("add",      "add a track to the end"),
        "q": ("add next", "queue a track to play next"),
        "r": ("remove",   "remove current track"),
        "s": ("shuffle",  "shuffle the playlist"),
        "x": ("exit",     "quit"),
    }

    print("\n🎵  Playlist Manager")
    print("Commands: " + "  |  ".join(f"[{k}] {v[0]}" for k, v in commands.items()))
    pl.display()

    while True:
        now = pl.now_playing
        prompt = f"Now playing: {now.title if now else 'nothing'} > "
        cmd = input(prompt).strip().lower()

        if cmd == "l":
            pl.display()
        elif cmd == "n":
            t = pl.next_track()
            print(f"⏭  {t}" if t else "⚠  End of playlist.")
        elif cmd == "p":
            t = pl.previous_track()
            print(f"⏮  {t}" if t else "⚠  Already at the start.")
        elif cmd == "a":
            title  = input("  Title: ").strip()
            artist = input("  Artist: ").strip()
            dur    = int(input("  Duration (seconds): ").strip())
            pl.add(Track(title, artist, dur))
            print("  ✓ Added.")
        elif cmd == "q":
            title  = input("  Title: ").strip()
            artist = input("  Artist: ").strip()
            dur    = int(input("  Duration (seconds): ").strip())
            pl.add_next(Track(title, artist, dur))
            print("  ✓ Queued next.")
        elif cmd == "r":
            if pl.now_playing:
                removed = pl.now_playing
                pl.remove(removed)
                print(f"  ✓ Removed '{removed.title}'.")
            else:
                print("  Nothing playing.")
        elif cmd == "s":
            pl.shuffle()
            pl.display()
        elif cmd == "x":
            print("👋  Bye.")
            break
        else:
            print("  Unknown command.")


if __name__ == "__main__":
    run_cli()
