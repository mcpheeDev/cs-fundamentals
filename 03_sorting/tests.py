from sorting import bubble_sort, insertion_sort, merge_sort
import random

passed = 0
failed = 0

def test(name, got, expected):
    global passed, failed
    if got == expected:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  {name}")
        print(f"       expected: {expected!r}")
        print(f"       got:      {got!r}")
        failed += 1

def test_true(name, condition):
    test(name, condition, True)


CASES = [
    [],
    [1],
    [2, 1],
    [3, 1, 2],
    [64, 34, 25, 12, 22, 11, 90],
    [5, 5, 5, 5],
    list(range(10, 0, -1)),   # reverse sorted
    list(range(10)),           # already sorted
]

for fn_name, fn in [("bubble_sort", bubble_sort),
                     ("insertion_sort", insertion_sort),
                     ("merge_sort", merge_sort)]:
    print(f"\n── {fn_name} ────────────────────────────────────────")

    for arr in CASES:
        expected = sorted(arr)
        result   = fn(arr)
        # handle both (sorted, c, s) and just sorted
        actual   = result[0] if isinstance(result, tuple) else result
        test(f"sorts {arr}", actual, expected)

    # original not modified
    original = [3, 1, 2]
    fn(original)
    test("does not modify original", original, [3, 1, 2])

    # comparisons and swaps are non-negative integers
    result = fn([5, 3, 1, 4, 2])
    if isinstance(result, tuple) and len(result) >= 2:
        test_true("comparisons is non-negative int",
                  isinstance(result[1], int) and result[1] >= 0)

    # large random test
    big = random.sample(range(1000), 200)
    result = fn(big)
    actual = result[0] if isinstance(result, tuple) else result
    test("sorts 200 random elements correctly", actual, sorted(big))


print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
