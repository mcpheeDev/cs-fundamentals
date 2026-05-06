# 06 – Banking System

## What you're building
A full banking system with multiple account types and a CLI.

## Account hierarchy

```
Account  (abstract base class)
  ├── CurrentAccount   — overdraft facility, monthly fee
  ├── SavingsAccount   — interest rate, withdrawal limit per month
  └── ISA              — tax-free, £20,000 annual deposit limit
```

## Requirements

### Account (abstract)
- Private attributes: `__account_number`, `__owner`, `__balance`
- Auto-incrementing account numbers (use a class variable)
- `deposit(amount)` and `withdraw(amount)` — both abstract
- `balance` property — read only, no setter
- Transaction log — every deposit/withdrawal recorded with timestamp
- `statement(last_n=None)` — print the last n transactions (all if None)

### CurrentAccount
- `overdraft_limit` — default £500
- Allow balance to go negative up to the overdraft limit
- `apply_overdraft_fee(fee)` — charge a fee if balance is negative

### SavingsAccount
- `interest_rate` — e.g. 0.04 (4% AER)
- Max 3 withdrawals per month — raise an error if exceeded
- `apply_interest()` — add monthly interest (rate / 12)

### ISA
- Annual deposit limit of £20,000 — raise an error if exceeded
- `new_tax_year()` — reset the annual allowance
- `apply_interest()` — like savings

### Bank class
- `open_account(account)` — register an account
- `transfer(from_number, to_number, amount)` — move money between accounts
- `summary()` — print all accounts and total deposits held

## Run tests
```bash
python3 tests.py
```
