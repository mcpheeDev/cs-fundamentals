from recursion import (factorial_recursive, factorial_iterative,
                        fib_naive, fib_memoised, fib_iterative,
                        sum_to_n_recursive, sum_to_n_iterative,
                        calculate_recursive, calculate_iterative,
                        power_recursive, power_iterative,
                        flatten, binary_search, merge_sort)

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


print("\n── Factorial ─────────────────────────────────────────")
for n, expected in [(0,1),(1,1),(5,120),(10,3628800)]:
    test(f"recursive {n}!", factorial_recursive(n), expected)
    test(f"iterative {n}!", factorial_iterative(n), expected)

print("\n── Fibonacci ─────────────────────────────────────────")
expected_seq = [0,1,1,2,3,5,8,13,21,34]
for i, exp in enumerate(expected_seq):
    test(f"naive fib({i})",     fib_naive(i),     exp)
    test(f"memoised fib({i})",  fib_memoised(i),  exp)
    test(f"iterative fib({i})", fib_iterative(i), exp)

print("\n── sum_to_n ──────────────────────────────────────────")
for n, exp in [(0,0),(1,1),(5,15),(10,55)]:
    test(f"recursive sum_to_n({n})", sum_to_n_recursive(n), exp)
    test(f"iterative sum_to_n({n})", sum_to_n_iterative(n), exp)

print("\n── calculate ─────────────────────────────────────────")
cases = [(0,5,5),(1,5,6),(4,10,20),(3,0,6)]
for a, b, exp in cases:
    test(f"recursive calculate({a},{b})", calculate_recursive(a,b), exp)
    test(f"iterative calculate({a},{b})", calculate_iterative(a,b), exp)

print("\n── power ─────────────────────────────────────────────")
for base, exp, result in [(2,0,1),(2,3,8),(3,4,81),(5,1,5)]:
    test(f"recursive power({base},{exp})", power_recursive(base,exp), result)
    test(f"iterative power({base},{exp})", power_iterative(base,exp), result)

print("\n── flatten ───────────────────────────────────────────")
test("flatten flat list",   flatten([1,2,3]),          [1,2,3])
test("flatten one level",   flatten([1,[2,3]]),         [1,2,3])
test("flatten deep",        flatten([1,[2,[3,[4]]]]),   [1,2,3,4])
test("flatten mixed",       flatten([1,[2,[3,4]],5]),   [1,2,3,4,5])
test("flatten empty",       flatten([]),                [])

print("\n── binary_search ─────────────────────────────────────")
arr = [2, 5, 8, 12, 16, 23, 38, 45, 62, 80]
for target, expected in [(23,5),(2,0),(80,9),(1,-1),(100,-1)]:
    test(f"binary_search {target}", binary_search(arr, target), expected)

print("\n── merge_sort ────────────────────────────────────────")
import random
for arr in [[],[1],[2,1],[3,1,4,1,5,9,2,6]]:
    test(f"sorts {arr}", merge_sort(arr), sorted(arr))
big = random.sample(range(1000), 100)
test("sorts 100 random elements", merge_sort(big), sorted(big))

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
