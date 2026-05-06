# 01 – Linked List

## What you're building
A **doubly-linked list** from scratch, then two real applications built on top of it.

## Part 1 — The linked list itself (`linked_list.py`)
Implement a doubly-linked list with:
- `append(data)` — add to the tail
- `prepend(data)` — add to the head
- `insert_after(target, data)` — insert after a specific value
- `remove(data)` — remove the first node with that value
- `find(data)` — return the node containing data, or None
- `display()` — print: `HEAD → A ↔ B ↔ C → TAIL`
- `__len__` and `__iter__`

## Part 2 — Music Playlist (`playlist.py`)
Build a playlist manager using your linked list. It needs:
- `add(track)` — add to end
- `add_next(track)` — insert after currently playing track
- `remove(track)` — remove a track
- `next_track()` / `previous_track()` — move through the playlist
- `shuffle()` — randomise the order
- `display()` — show all tracks, marking the current one with ▶

A `Track` should store: title, artist, duration (seconds).

## Part 3 — Browser History (`browser_history.py`)
Build a browser back/forward history using your linked list:
- `visit(url)` — navigate to a new URL, clearing any forward history
- `back()` — go back one page
- `forward()` — go forward one page
- `display()` — show full history, marking current page

## Run tests
```bash
python3 tests.py
```
