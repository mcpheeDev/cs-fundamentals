"""
bank.py — A full banking system demonstrating OOP encapsulation and inheritance.

Account hierarchy:
  Account (abstract base)
    ├── CurrentAccount   — overdraft facility
    ├── SavingsAccount   — interest rate, withdrawal limit
    └── ISA              — tax-free, annual deposit limit

Run:  python3 bank.py
"""

from abc import ABC, abstractmethod
from datetime import datetime
import random


# ══════════════════════════════════════════════════════════════════════════════
# TRANSACTION LOG
# ══════════════════════════════════════════════════════════════════════════════

class Transaction:
    def __init__(self, kind, amount, balance_after, description=""):
        self.kind        = kind           # "credit" or "debit"
        self.amount      = amount
        self.balance     = balance_after
        self.description = description
        self.timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        sign = "+" if self.kind == "credit" else "-"
        return (f"  {self.timestamp}  {sign}£{self.amount:>8.2f}  "
                f"Balance: £{self.balance:>10.2f}  {self.description}")


# ══════════════════════════════════════════════════════════════════════════════
# ACCOUNT BASE CLASS
# ══════════════════════════════════════════════════════════════════════════════

class Account(ABC):
    _next_account_number = 10000001

    def __init__(self, owner_name, initial_deposit=0):
        self.__account_number = Account._next_account_number
        Account._next_account_number += 1
        self.__owner       = owner_name
        self.__balance     = 0.0
        self.__transactions = []
        if initial_deposit > 0:
            self._credit(initial_deposit, "Initial deposit")

    # ── Private helpers ───────────────────────────────────────────────────────
    def _credit(self, amount, description=""):
        self.__balance += amount
        self.__transactions.append(
            Transaction("credit", amount, self.__balance, description))

    def _debit(self, amount, description=""):
        self.__balance -= amount
        self.__transactions.append(
            Transaction("debit", amount, self.__balance, description))

    # ── Public getters (encapsulation) ────────────────────────────────────────
    @property
    def account_number(self): return self.__account_number
    @property
    def owner(self):          return self.__owner
    @property
    def balance(self):        return self.__balance

    # ── Abstract interface — subclasses define the rules ──────────────────────
    @abstractmethod
    def deposit(self, amount):  pass

    @abstractmethod
    def withdraw(self, amount): pass

    @abstractmethod
    def account_type(self):     pass

    # ── Shared behaviour ──────────────────────────────────────────────────────
    def statement(self, last_n=None):
        txns = self.__transactions[-last_n:] if last_n else self.__transactions
        print(f"\n{'═'*65}")
        print(f"  {self.account_type()}  |  #{self.account_number}  |  {self.owner}")
        print(f"  Balance: £{self.balance:,.2f}")
        print(f"{'─'*65}")
        if txns:
            for t in txns:
                print(t)
        else:
            print("  No transactions.")
        print(f"{'═'*65}\n")

    def __str__(self):
        return (f"{self.account_type()} #{self.account_number} "
                f"[{self.owner}]  £{self.balance:,.2f}")


# ══════════════════════════════════════════════════════════════════════════════
# SUBCLASSES
# ══════════════════════════════════════════════════════════════════════════════

class CurrentAccount(Account):
    """Everyday account with an overdraft facility."""

    def __init__(self, owner_name, initial_deposit=0, overdraft_limit=500):
        self.__overdraft_limit = overdraft_limit
        super().__init__(owner_name, initial_deposit)

    def account_type(self):
        return "Current Account"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._credit(amount, "Deposit")
        print(f"  ✓ Deposited £{amount:.2f} → balance £{self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < -self.__overdraft_limit:
            raise ValueError(
                f"Exceeds overdraft limit of £{self.__overdraft_limit:.2f}")
        self._debit(amount, "Withdrawal")
        print(f"  ✓ Withdrew £{amount:.2f} → balance £{self.balance:.2f}"
              + ("  ⚠ In overdraft" if self.balance < 0 else ""))

    def apply_overdraft_fee(self, fee=5.00):
        if self.balance < 0:
            self._debit(fee, "Overdraft fee")
            print(f"  ⚠ Overdraft fee £{fee:.2f} applied")


class SavingsAccount(Account):
    """High-interest savings with a monthly withdrawal limit."""

    WITHDRAWAL_LIMIT_PER_MONTH = 3

    def __init__(self, owner_name, initial_deposit=0, interest_rate=0.04):
        self.__interest_rate     = interest_rate
        self.__withdrawals_this_month = 0
        super().__init__(owner_name, initial_deposit)

    def account_type(self):
        return "Savings Account"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._credit(amount, "Deposit")
        print(f"  ✓ Deposited £{amount:.2f} → balance £{self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.__withdrawals_this_month >= self.WITHDRAWAL_LIMIT_PER_MONTH:
            raise ValueError(
                f"Monthly withdrawal limit ({self.WITHDRAWAL_LIMIT_PER_MONTH}) reached")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self._debit(amount, "Withdrawal")
        self.__withdrawals_this_month += 1
        remaining = self.WITHDRAWAL_LIMIT_PER_MONTH - self.__withdrawals_this_month
        print(f"  ✓ Withdrew £{amount:.2f} → balance £{self.balance:.2f}  "
              f"({remaining} withdrawal(s) remaining this month)")

    def apply_interest(self):
        """Apply annual interest (call monthly with 1/12 rate)."""
        interest = self.balance * (self.__interest_rate / 12)
        self._credit(round(interest, 2), f"Interest ({self.__interest_rate*100:.1f}% AER)")
        print(f"  ✓ Interest £{interest:.2f} applied → balance £{self.balance:.2f}")

    def reset_monthly_withdrawals(self):
        self.__withdrawals_this_month = 0


class ISA(Account):
    """Individual Savings Account — tax-free with an annual deposit limit."""

    ANNUAL_LIMIT = 20_000

    def __init__(self, owner_name, initial_deposit=0, interest_rate=0.05):
        self.__interest_rate    = interest_rate
        self.__deposited_this_year = 0
        super().__init__(owner_name, min(initial_deposit, self.ANNUAL_LIMIT))
        self.__deposited_this_year = min(initial_deposit, self.ANNUAL_LIMIT)

    def account_type(self):
        return "Cash ISA"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        remaining_allowance = self.ANNUAL_LIMIT - self.__deposited_this_year
        if amount > remaining_allowance:
            raise ValueError(
                f"Exceeds annual ISA limit. Remaining allowance: £{remaining_allowance:,.2f}")
        self._credit(amount, "ISA Deposit (tax-free)")
        self.__deposited_this_year += amount
        print(f"  ✓ Deposited £{amount:.2f} → balance £{self.balance:.2f}  "
              f"(£{remaining_allowance - amount:,.2f} allowance remaining)")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self._debit(amount, "ISA Withdrawal")
        print(f"  ✓ Withdrew £{amount:.2f} → balance £{self.balance:.2f}")

    def apply_interest(self):
        interest = self.balance * (self.__interest_rate / 12)
        self._credit(round(interest, 2),
                     f"Tax-free interest ({self.__interest_rate*100:.1f}% AER)")
        print(f"  ✓ Interest £{interest:.2f} applied")

    def new_tax_year(self):
        self.__deposited_this_year = 0
        print("  ✓ New tax year — ISA allowance reset to £20,000")


# ══════════════════════════════════════════════════════════════════════════════
# BANK
# ══════════════════════════════════════════════════════════════════════════════

class Bank:
    def __init__(self, name):
        self.__name     = name
        self.__accounts = {}

    def open_account(self, account: Account):
        self.__accounts[account.account_number] = account
        print(f"  ✓ Opened {account}")
        return account

    def get_account(self, account_number: int) -> Account:
        acc = self.__accounts.get(account_number)
        if not acc:
            raise KeyError(f"Account #{account_number} not found")
        return acc

    def transfer(self, from_number, to_number, amount):
        src = self.get_account(from_number)
        dst = self.get_account(to_number)
        src.withdraw(amount)
        dst.deposit(amount)
        print(f"  ↔  Transferred £{amount:.2f}: "
              f"#{from_number} → #{to_number}")

    def summary(self):
        total = sum(a.balance for a in self.__accounts.values())
        print(f"\n{'═'*55}")
        print(f"  {self.__name}  —  {len(self.__accounts)} accounts")
        print(f"{'─'*55}")
        for acc in self.__accounts.values():
            print(f"  {acc}")
        print(f"{'─'*55}")
        print(f"  Total deposits held: £{total:,.2f}")
        print(f"{'═'*55}\n")


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    bank = Bank("PyBank")

    alice_current = bank.open_account(CurrentAccount("Alice Chen",  2000))
    alice_isa     = bank.open_account(ISA("Alice Chen",             5000))
    bob_savings   = bank.open_account(SavingsAccount("Bob Smith",   1000, interest_rate=0.035))

    print("\n--- Deposits & Withdrawals ---")
    alice_current.deposit(500)
    alice_current.withdraw(200)
    try:
        alice_current.withdraw(5000)   # exceeds overdraft
    except ValueError as e:
        print(f"  ✗ {e}")

    print("\n--- Savings interest ---")
    for _ in range(3):
        bob_savings.apply_interest()

    print("\n--- ISA limit ---")
    try:
        alice_isa.deposit(20000)   # over annual limit
    except ValueError as e:
        print(f"  ✗ {e}")

    print("\n--- Transfer ---")
    bank.transfer(alice_current.account_number, bob_savings.account_number, 300)

    alice_current.statement()
    bob_savings.statement()
    bank.summary()
