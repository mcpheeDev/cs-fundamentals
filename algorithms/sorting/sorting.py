"""
sorting.py — Bubble sort, insertion sort, and merge sort with a live
ASCII step-by-step visualiser and a performance benchmarker.

Run:  python3 sorting.py
"""

import time
import random


# ── ASCII Visualiser ──────────────────────────────────────────────────────────

def _bar(value, max_value, width=30):
    filled = int(value / max_value * width)
    return "█" * filled + "░" * (width - filled)

def visualise(arr, highlight=(), label=""):
    """Print a horizontal bar chart of the array state."""
    max_val = max(arr) if arr else 1
    print(f"\n  {label}")
    for i, v in enumerate(arr):
        marker = " ◀" if i in highlight else ""
        print(f"  [{i:>2}] {_bar(v, max_val)} {v:>3}{marker}")


# ── Bubble Sort ───────────────────────────────────────────────────────────────

def bubble_sort(arr, show_steps=False):
    """
    Bubble sort — O(n²) average/worst, O(n) best (already sorted).
    Repeatedly swaps adjacent elements that are out of order.
    """
    arr = arr[:]
    n = len(arr)
    comparisons = swaps = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
                if show_steps:
                    visualise(arr, highlight=(j, j + 1),
                              label=f"Pass {i+1}  swap [{j}]↔[{j+1}]")
        if not swapped:
            break   # already sorted

    return arr, comparisons, swaps


# ── Insertion Sort ────────────────────────────────────────────────────────────

def insertion_sort(arr, show_steps=False):
    """
    Insertion sort — O(n²) average/worst, O(n) best.
    Builds a sorted prefix by inserting each element into its correct position.
    """
    arr = arr[:]
    comparisons = swaps = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        comparisons += 1   # final comparison that broke the loop
        arr[j + 1] = key
        if show_steps:
            visualise(arr, highlight=(j + 1,),
                      label=f"Insert {key} → position {j+1}")

    return arr, comparisons, swaps


# ── Merge Sort ────────────────────────────────────────────────────────────────

def merge_sort(arr, depth=0, show_steps=False):
    """
    Merge sort — O(n log n) all cases. Divide-and-conquer recursive.
    """
    if len(arr) <= 1:
        return arr[:], 0, 0

    mid = len(arr) // 2
    left,  c1, s1 = merge_sort(arr[:mid],  depth + 1, show_steps)
    right, c2, s2 = merge_sort(arr[mid:],  depth + 1, show_steps)

    merged, c3, s3 = _merge(left, right)
    comparisons = c1 + c2 + c3
    swaps = s1 + s2 + s3

    if show_steps and depth == 0:
        visualise(merged, label="Merged result")

    return merged, comparisons, swaps


def _merge(left, right):
    result = []
    i = j = comparisons = swaps = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
            swaps += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result, comparisons, swaps


# ── Benchmark ─────────────────────────────────────────────────────────────────

def benchmark(sizes=(100, 500, 1000, 3000)):
    algorithms = [
        ("Bubble sort",    bubble_sort),
        ("Insertion sort", insertion_sort),
        ("Merge sort",     merge_sort),
    ]

    header = f"{'Size':>6}  " + "  ".join(f"{name:>18}" for name, _ in algorithms)
    print("\n" + "=" * len(header))
    print("SORT BENCHMARK — time in milliseconds")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for n in sizes:
        data = [random.randint(1, 1000) for _ in range(n)]
        row = f"{n:>6}  "
        for name, fn in algorithms:
            start = time.perf_counter()
            fn(data[:])
            elapsed = (time.perf_counter() - start) * 1000
            row += f"  {elapsed:>16.2f}ms"
        print(row)
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]

    print("=" * 50)
    print("BUBBLE SORT — step by step")
    print("=" * 50)
    print("Start:", sample)
    result, comps, swaps = bubble_sort(sample, show_steps=True)
    print(f"\nSorted: {result}  |  comparisons={comps}  swaps={swaps}")

    print("\n" + "=" * 50)
    print("INSERTION SORT — step by step")
    print("=" * 50)
    print("Start:", sample)
    result, comps, swaps = insertion_sort(sample, show_steps=True)
    print(f"\nSorted: {result}  |  comparisons={comps}  swaps={swaps}")

    print("\n" + "=" * 50)
    print("MERGE SORT")
    print("=" * 50)
    print("Start:", sample)
    result, comps, swaps = merge_sort(sample, show_steps=True)
    print(f"Sorted: {result}  |  comparisons={comps}  merge-ops={swaps}")

    benchmark()
