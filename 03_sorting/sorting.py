import time
import random


# ── Visualiser helper (use this inside your sorts if you want) ────────────────

def visualise(arr, highlight=(), label=""):
    """Print the array as horizontal bars. highlight = tuple of indices to mark."""
    max_val = max(arr) if arr else 1
    print(f"\n  {label}")
    for i, v in enumerate(arr):
        filled = int(v / max_val * 20)
        bar    = "█" * filled + "░" * (20 - filled)
        marker = "  ◀" if i in highlight else ""
        print(f"  [{i:>2}] {bar} {v:>4}{marker}")


# ── Bubble Sort ───────────────────────────────────────────────────────────────

def bubble_sort(arr, show_steps=False):
    """
    TODO: implement bubble sort.

    - Work on a copy of arr (don't modify the original)
    - If show_steps is True, call visualise() after each swap
    - Return (sorted_list, comparisons, swaps)

    Hints:
      - Outer loop: n-1 passes
      - Inner loop: shrinks each pass (last i elements are already sorted)
      - Early exit: if no swaps in a pass, the list is sorted
    """
    arr = arr[:]
    comparisons = 0
    swaps       = 0

    # TODO

    return arr, comparisons, swaps


# ── Insertion Sort ────────────────────────────────────────────────────────────

def insertion_sort(arr, show_steps=False):
    """
    TODO: implement insertion sort.

    - Work on a copy of arr
    - If show_steps is True, call visualise() after each insertion
    - Return (sorted_list, comparisons, swaps)

    Hints:
      - Start from index 1
      - Save arr[i] as 'key'
      - Shift elements larger than key one position to the right
      - Place key in the gap you created
    """
    arr = arr[:]
    comparisons = 0
    swaps       = 0

    # TODO

    return arr, comparisons, swaps


# ── Merge Sort ────────────────────────────────────────────────────────────────

def merge_sort(arr):
    """
    TODO: implement merge sort recursively.

    - Return (sorted_list, comparisons, swaps)
    - Base case: a list of 0 or 1 elements is already sorted
    - Split arr in half, recursively sort each half
    - Merge the two sorted halves together

    Hint: write a helper _merge(left, right) that merges two
    sorted lists into one sorted list, counting comparisons.
    """
    # TODO
    pass


def _merge(left, right):
    """
    TODO: merge two sorted lists into one sorted list.
    Return (merged_list, comparisons, swaps).
    """
    # TODO
    pass


# ── Benchmarker ───────────────────────────────────────────────────────────────

def benchmark(sizes=(100, 500, 1000, 3000)):
    """
    TODO: time bubble_sort, insertion_sort, and merge_sort on random arrays
    of each size. Print a formatted comparison table like:

      Size    Bubble sort    Insertion sort    Merge sort
      ────────────────────────────────────────────────────
       100        1.23ms            0.98ms        0.21ms
       500       31.45ms           24.12ms        1.23ms
      ...
    """
    # TODO
    pass


if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]

    print("Bubble sort (step by step):")
    result, c, s = bubble_sort(sample, show_steps=True)
    print(f"Sorted: {result}  comparisons={c}  swaps={s}")

    print("\nInsertion sort (step by step):")
    result, c, s = insertion_sort(sample, show_steps=True)
    print(f"Sorted: {result}  comparisons={c}  swaps={s}")

    print("\nMerge sort:")
    result, c, s = merge_sort(sample)
    print(f"Sorted: {result}  comparisons={c}")

    benchmark()
