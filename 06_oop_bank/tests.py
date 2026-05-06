from bank import CurrentAccount, SavingsAccount, ISA, Bank

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

def test_raises(name, fn, err):
    global passed, failed
    try:
        fn()
        print(f"  ✗  {name}  (no exception raised)")
        failed += 1
    except err:
        print(f"  ✓  {name}")
        passed += 1


print("\n── Account numbers ───────────────────────────────────")
a1 = CurrentAccount("Alice")
a2 = CurrentAccount("Bob")
test_true("account numbers are unique", a1.account_number != a2.account_number)
test_true("account number auto-increments",
          a2.account_number == a1.account_number + 1)

print("\n── Encapsulation ─────────────────────────────────────")
test_raises("balance not directly settable",
            lambda: setattr(a1, "balance", 9999), (AttributeError, TypeError))

print("\n── CurrentAccount ────────────────────────────────────")
c = CurrentAccount("Test", initial_deposit=1000)
test("initial deposit sets balance", c.balance, 1000)
c.deposit(500)
test("deposit increases balance", c.balance, 1500)
c.withdraw(200)
test("withdraw decreases balance", c.balance, 1300)

test_raises("deposit ≤ 0 raises ValueError",
            lambda: c.deposit(-10), ValueError)
test_raises("withdraw ≤ 0 raises ValueError",
            lambda: c.withdraw(-5), ValueError)
test_raises("over-overdraft raises ValueError",
            lambda: c.withdraw(99999), ValueError)

# Overdraft allowed up to limit
c2 = CurrentAccount("Overdraft", initial_deposit=100, overdraft_limit=500)
c2.withdraw(500)   # puts balance at -400, within limit
test_true("overdraft within limit allowed", c2.balance < 0)

print("\n── SavingsAccount ────────────────────────────────────")
s = SavingsAccount("Saver", initial_deposit=1000, interest_rate=0.12)
before = s.balance
s.apply_interest()
test_true("interest increases balance", s.balance > before)
expected_interest = round(1000 * 0.12 / 12, 2)
test("interest amount correct", round(s.balance - before, 2), expected_interest)

s.withdraw(100)
s.withdraw(100)
s.withdraw(100)
test_raises("4th withdrawal in month raises ValueError",
            lambda: s.withdraw(1), ValueError)

s.reset_monthly_withdrawals()
s.withdraw(10)   # should work now
test_true("withdrawal works after reset", True)

print("\n── ISA ───────────────────────────────────────────────")
isa = ISA("Investor", initial_deposit=10000)
test("initial deposit within limit", isa.balance, 10000)
test_raises("over annual limit raises ValueError",
            lambda: isa.deposit(15000), ValueError)
isa.new_tax_year()
isa.deposit(15000)   # now allowed — new year reset the allowance
test_true("deposit allowed after new tax year", isa.balance > 10000)

print("\n── Bank transfer ─────────────────────────────────────")
bank = Bank("Test")
b1 = bank.open_account(CurrentAccount("Alice", 1000))
b2 = bank.open_account(SavingsAccount("Bob",   500))
bank.transfer(b1.account_number, b2.account_number, 200)
test("source debited",  b1.balance, 800)
test("target credited", b2.balance, 700)
test_raises("transfer from unknown account raises KeyError",
            lambda: bank.transfer(9999999, b2.account_number, 10), KeyError)

print(f"\n{'═'*45}")
print(f"  {passed} passed  |  {failed} failed")
print(f"{'═'*45}\n")
