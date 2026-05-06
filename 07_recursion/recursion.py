import functools
import time

# ── Tier 1: Classics ──────────────────────────────────────────────────────────

def factorial_recursive(n):
    # TODO: base case n==0 → 1, else n * factorial(n-1)
    pass

def factorial_iterative(n):
    # TODO: same result using a loop
    pass

def fib_naive(n):
    # TODO: base case n<=1, else fib(n-1)+fib(n-2)
    # WARNING: do not call this for n > 35, it gets very slow
    pass

@functools.lru_cache(maxsize=None)
def fib_memoised(n):
    # TODO: same recursion as fib_naive but decorated with lru_cache
    pass

def fib_iterative(n):
    # TODO: O(n) time, O(1) space — use two variables
    pass

def sum_to_n_recursive(n):
    # TODO
    pass

def sum_to_n_iterative(n):
    # TODO
    pass

# ── Tier 2: Conversions ───────────────────────────────────────────────────────

def calculate_recursive(a, b):
    if a == 0:
        return b
    return calculate_recursive(a - 1, a + b)

def calculate_iterative(a, b):
    # TODO: rewrite calculate without recursion
    pass

def power_recursive(base, exp):
    # TODO: base case exp==0 → 1, else base * power(base, exp-1)
    pass

def power_iterative(base, exp):
    # TODO
    pass

def count_down_recursive(n):
    # TODO: print n, then recurse with n-1, print "Go!" at base case
    pass

def count_down_iterative(n):
    # TODO
    pass

# ── Tier 3: Applied ───────────────────────────────────────────────────────────

def flatten(nested):
    # TODO: recursively flatten a nested list of any depth
    # [1, [2, [3, 4]], 5] → [1, 2, 3, 4, 5]
    pass

def binary_search(arr, target, lo=None, hi=None):
    # TODO: recursive binary search
    # return the index of target, or -1 if not found
    # initialise lo=0, hi=len(arr)-1 on first call
    pass

def merge_sort(arr):
    # TODO: recursive merge sort — return a sorted copy
    pass

# ── Benchmarks ────────────────────────────────────────────────────────────────

def benchmark_fibonacci():
    """TODO: time fib_naive, fib_memoised, and fib_iterative for n=10,20,30,35.
    Print a formatted comparison table."""
    pass

if __name__ == "__main__":
    print("calculate(4, 10) =", calculate_recursive(4, 10))
    print("calculate_iterative(4, 10) =", calculate_iterative(4, 10))
    print("flatten([1,[2,[3,4]],5]) =", flatten([1, [2, [3, 4]], 5]))
    benchmark_fibonacci()
