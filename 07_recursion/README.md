# 07 – Recursion Toolkit

## What you're building
A set of recursive functions, each also implemented iteratively,
with timing comparisons to show where each approach wins.

## Functions to implement (`recursion.py`)

### Tier 1 — Classics
- `factorial(n)` — recursive and iterative versions
- `fibonacci(n)` — naive recursive, memoised, iterative
- `sum_to_n(n)` — recursive and iterative

### Tier 2 — Conversions
The exam asks you to rewrite recursive functions as iterative ones.
For each function below, implement BOTH versions:
- `calculate(a, b)` — from the spec: if a==0 return b, else calculate(a-1, a+b)
- `power(base, exp)` — base^exp without using **
- `count_down(n)` — print n, n-1, ..., 1 then "Go!"

### Tier 3 — Applied
- `flatten(nested_list)` — flatten an arbitrarily nested list
  e.g. [1, [2, [3, 4]], 5] → [1, 2, 3, 4, 5]
- `binary_search(arr, target, lo, hi)` — recursive binary search
- `merge_sort(arr)` — recursive (you may have done this in 03_sorting)

### Benchmarks
Time naive vs memoised fibonacci for n = 10, 20, 30, 35.
Show how memoisation turns O(2^n) into O(n).

## Run tests
```bash
python3 tests.py
```
