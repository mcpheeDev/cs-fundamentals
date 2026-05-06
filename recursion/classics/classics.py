"""
classics.py — Classic recursion problems with timing comparisons
and an ASCII Tower of Hanoi visualiser.

Run:  python3 classics.py
"""

import time
import functools
import sys

sys.setrecursionlimit(5000)


# ══════════════════════════════════════════════════════════════════════════════
# FACTORIAL  — recursive vs iterative
# ══════════════════════════════════════════════════════════════════════════════

def factorial_recursive(n):
    """O(n) time, O(n) space (call stack)."""
    if n < 0:   raise ValueError("Factorial undefined for negative numbers")
    if n == 0:  return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n):
    """O(n) time, O(1) space."""
    if n < 0:   raise ValueError("Factorial undefined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@functools.lru_cache(maxsize=None)
def factorial_memoised(n):
    """O(n) first call, O(1) cached calls — demonstrates memoisation."""
    if n == 0: return 1
    return n * factorial_memoised(n - 1)


# ══════════════════════════════════════════════════════════════════════════════
# FIBONACCI  — naive recursive, memoised, iterative
# ══════════════════════════════════════════════════════════════════════════════

def fib_naive(n):
    """O(2^n) — exponential, extremely slow for large n."""
    if n <= 1: return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fib_memoised(n):
    """O(n) time after caching — dramatic speedup over naive."""
    if n <= 1: return n
    return fib_memoised(n - 1) + fib_memoised(n - 2)


def fib_iterative(n):
    """O(n) time, O(1) space — most efficient."""
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fib_sequence(n, fn=fib_iterative):
    """Return the first n Fibonacci numbers."""
    return [fn(i) for i in range(n)]


# ══════════════════════════════════════════════════════════════════════════════
# TOWER OF HANOI  — with ASCII visualiser
# ══════════════════════════════════════════════════════════════════════════════

class Hanoi:
    """
    Tower of Hanoi solver with a live ASCII peg visualiser.

    The classic recursive insight:
      To move n disks from A to C using B as auxiliary:
        1. Move n-1 disks from A to B  (using C)
        2. Move disk n from A to C
        3. Move n-1 disks from B to C  (using A)

    Minimum moves: 2^n - 1
    """

    DISK_CHARS = ["▓", "▒", "░"]

    def __init__(self, n_disks, animate=True):
        if n_disks > 8:
            raise ValueError("Max 8 disks for readable visualisation")
        self.n        = n_disks
        self.animate  = animate
        self.pegs     = {
            "A": list(range(n_disks, 0, -1)),   # largest disk at bottom
            "B": [],
            "C": [],
        }
        self.moves    = 0
        self.history  = []

    def _draw(self):
        height = self.n + 1
        width  = self.n * 2 + 3
        print()
        for level in range(height, 0, -1):
            row = ""
            for peg in ("A", "B", "C"):
                stack = self.pegs[peg]
                if level <= len(stack):
                    disk = stack[level - 1]
                    char = "█"
                    seg  = char * disk
                    row += f"{seg:^{width}}"
                else:
                    row += f"{'|':^{width}}"
            print(row)
        # Base and labels
        base = "═" * width
        print(base + base + base)
        labels = "".join(f"{'A':^{width}}" if p == "A" else
                         f"{'B':^{width}}" if p == "B" else
                         f"{'C':^{width}}" for p in ("A", "B", "C"))
        print(labels)
        print(f"  Move {self.moves}  |  "
              f"A={self.pegs['A']}  B={self.pegs['B']}  C={self.pegs['C']}")

    def _move_disk(self, source, target):
        disk = self.pegs[source].pop()
        self.pegs[target].append(disk)
        self.moves += 1
        self.history.append((source, target, disk))
        if self.animate:
            print(f"\n  Move {self.moves}: disk {disk}  {source} → {target}")
            self._draw()

    def solve(self, n=None, source="A", target="C", aux="B"):
        if n is None:
            n = self.n
            if self.animate:
                print(f"\n{'═'*50}")
                print(f"  Tower of Hanoi  —  {n} disks")
                print(f"  Minimum moves required: {2**n - 1}")
                print(f"{'═'*50}")
                self._draw()
        if n == 0:
            return
        self.solve(n - 1, source, aux, target)
        self._move_disk(source, target)
        self.solve(n - 1, aux, target, source)

    def summary(self):
        print(f"\n  Solved in {self.moves} moves  "
              f"(minimum possible: {2**self.n - 1})")


# ══════════════════════════════════════════════════════════════════════════════
# BENCHMARKING
# ══════════════════════════════════════════════════════════════════════════════

def _time(fn, *args, reps=3):
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter()
        fn(*args)
        best = min(best, time.perf_counter() - t)
    return best * 1000   # ms


def benchmark_fibonacci():
    print("\n" + "═"*55)
    print("  FIBONACCI BENCHMARK")
    print("═"*55)
    print(f"  {'n':>4}  {'Naive':>12}  {'Memoised':>12}  {'Iterative':>12}")
    print("  " + "─"*48)
    for n in [10, 20, 30, 35]:
        t_naive = _time(fib_naive,     n) if n <= 35 else float("inf")
        t_memo  = _time(fib_memoised,  n)
        t_iter  = _time(fib_iterative, n)
        naive_str = f"{t_naive:.3f}ms" if t_naive != float("inf") else "too slow"
        print(f"  {n:>4}  {naive_str:>12}  {t_memo:>10.4f}ms  {t_iter:>10.4f}ms")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Factorial demo
    print("=" * 50)
    print("FACTORIAL")
    print("=" * 50)
    for n in [0, 1, 5, 10, 15]:
        r = factorial_recursive(n)
        i = factorial_iterative(n)
        m = factorial_memoised(n)
        ok = r == i == m
        print(f"  {n}! = {r}  {'✓' if ok else '✗ MISMATCH'}")

    # Fibonacci demo
    print("\n" + "=" * 50)
    print("FIBONACCI SEQUENCE (first 12)")
    print("=" * 50)
    print(" ", fib_sequence(12))

    benchmark_fibonacci()

    # Tower of Hanoi
    h = Hanoi(n_disks=4, animate=True)
    h.solve()
    h.summary()

    print("\n\nMove count by disk count:")
    for n in range(1, 9):
        solver = Hanoi(n, animate=False)
        solver.solve()
        print(f"  {n} disks → {solver.moves} moves  "
              f"(2^{n}-1 = {2**n-1}) {'✓' if solver.moves == 2**n-1 else '✗'}")
