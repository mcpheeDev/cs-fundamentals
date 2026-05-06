# 03 – Sorting Algorithms

## What you're building
Three sorting algorithms from scratch, plus a visualiser and benchmarker.

## Part 1 — The algorithms (`sorting.py`)

### Bubble Sort
- Repeatedly compare adjacent elements and swap if out of order
- Each full pass "bubbles" the largest unsorted element to the end
- Optimise it: if no swaps happen in a pass, stop early
- Track and return the number of comparisons and swaps made

### Insertion Sort
- Build a sorted section from left to right
- For each element, shift larger elements right to make room
- Insert the element into its correct position
- Track comparisons and swaps

### Merge Sort
- Divide the list in half recursively until you have single elements
- Merge pairs of sorted halves back together
- This one is recursive — think about your base case carefully

## Part 2 — ASCII Visualiser
After each swap or insertion, print the current state of the array as
horizontal bars so you can watch the sort happen. Example:

```
[0] ████░░░░░░  40
[1] ██████████  100
[2] ██░░░░░░░░  20  ◀ swapped
```

## Part 3 — Benchmarker
Time all three algorithms on the same randomly generated arrays of
sizes 100, 500, 1000, 3000. Print a comparison table.

## Run tests
```bash
python3 tests.py
```
