from simulator import LMC, LMCAssembler, PROGRAMS, run_program

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


# ── Assembler ─────────────────────────────────────────────────────────────────
print("\n── Assembler ─────────────────────────────────────────")

asm = LMCAssembler()

# Simple program: INP, OUT, HLT
mc = asm.assemble("INP\nOUT\nHLT")
test_true("assemble returns a list", isinstance(mc, list))
test("INP encodes to 901", mc[0], 901)
test("OUT encodes to 902", mc[1], 902)
test("HLT encodes to 0",   mc[2], 0)

# ADD with operand
mc2 = asm.assemble("ADD 5\nHLT")
test("ADD 5 encodes to 105", mc2[0], 105)

# Labels
mc3 = asm.assemble("loop: INP\nBRA loop\nHLT")
test_true("assembles with labels", len(mc3) >= 3)
test("BRA loop resolves to address 0", mc3[1], 600)

# DAT
mc4 = asm.assemble("DAT 42")
test("DAT 42 stores 42", mc4[0], 42)

# Comments stripped
mc5 = asm.assemble("// this is a comment\nHLT")
test("comment stripped, HLT at address 0", mc5[0], 0)


# ── Simulator ─────────────────────────────────────────────────────────────────
print("\n── Simulator: basic execution ───────────────────────")

lmc = LMC()
# INP, OUT, HLT
lmc.load([901, 902, 0])
lmc.set_inputs(42)
outputs = lmc.run()
test("INP→OUT outputs the input", outputs, [42])

# ADD
lmc2 = LMC()
lmc2.load([901, 300+99, 901, 100+99, 902, 0])
# INP, STA 99, INP, ADD 99, OUT, HLT
lmc2.set_inputs(3, 7)
test("3 + 7 = 10", lmc2.run(), [10])

# SUB
lmc3 = LMC()
lmc3.load([901, 300+99, 901, 200+99, 902, 0])
lmc3.set_inputs(10, 4)
test("10 - 4 = 6", lmc3.run(), [6])

# BRZ
source_brz = """
        INP
        BRZ  done
        OUT
done:   HLT
"""
mc_brz = asm.assemble(source_brz)
lmc4 = LMC()
lmc4.load(mc_brz)
lmc4.set_inputs(0)
test("BRZ: input 0 skips OUT", lmc4.run(), [])

lmc5 = LMC()
lmc5.load(mc_brz)
lmc5.set_inputs(5)
test("BRZ: input 5 does OUT", lmc5.run(), [5])

print("\n── Your programs ─────────────────────────────────────")
# These tests will fail until you write the LMC programs

try:
    out = run_program("absolute_difference", 13, 5)
    test("abs_diff(13, 5) = 8", out, [8])
except Exception as e:
    print(f"  ✗  absolute_difference raised: {e}")
    failed += 1

try:
    out = run_program("absolute_difference", 3, 8)
    test("abs_diff(3, 8) = 5", out, [5])
except Exception as e:
    print(f"  ✗  absolute_difference raised: {e}")
    failed += 1

try:
    out = run_program("count_to_n", 5)
    test("count_to_n(5) outputs [1,2,3,4,5]", out, [1, 2, 3, 4, 5])
except Exception as e:
    print(f"  ✗  count_to_n raised: {e}")
    failed += 1

try:
    out = run_program("sum_to_n", 5)
    test("sum_to_n(5) = 15", out, [15])
except Exception as e:
    print(f"  ✗  sum_to_n raised: {e}")
    failed += 1

try:
    out = run_program("sum_to_n", 10)
    test("sum_to_n(10) = 55", out, [55])
except Exception as e:
    print(f"  ✗  sum_to_n raised: {e}")
    failed += 1

try:
    out = run_program("loop_until_three", 7, 2, 9, 3)
    test("loop_until_three stops at 3", out, [])
except Exception as e:
    print(f"  ✗  loop_until_three raised: {e}")
    failed += 1


print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
