from abc import ABC, abstractmethod
from datetime import datetime


class Transaction:
    def __init__(self, kind, amount, balance_after, description=""):
        self.kind        = kind    # "credit" or "debit"
        self.amount      = amount
        self.balance     = balance_after
        self.description = description
        self.timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        sign = "+" if self.kind == "credit" else "-"
        return (f"  {self.timestamp}  {sign}£{self.amount:>8.2f}  "
                f"Balance: £{self.balance:>10.2f}  {self.description}")


class Account(ABC):
    _next_number = 10000001   # class variable for auto-incrementing account numbers

    def __init__(self, owner_name, initial_deposit=0):
        # TODO: assign a unique account number (use _next_number, then increment it)
        # store owner_name as private attribute
        # store balance as private attribute, starting at 0
        # store transactions as a private list
        # if initial_deposit > 0, credit it
        pass

    @property
    def account_number(self):
        # TODO
        pass

    @property
    def owner(self):
        # TODO
        pass

    @property
    def balance(self):
        # TODO
        pass

    def _credit(self, amount, description=""):
        # TODO: increase balance, append Transaction to log
        pass

    def _debit(self, amount, description=""):
        # TODO: decrease balance, append Transaction to log
        pass

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def account_type(self):
        pass

    def statement(self, last_n=None):
        # TODO: print a formatted statement showing the last_n transactions
        # (all transactions if last_n is None)
        pass

    def __str__(self):
        return f"{self.account_type()} #{self.account_number} [{self.owner}]  £{self.balance:,.2f}"


class CurrentAccount(Account):
    def __init__(self, owner_name, initial_deposit=0, overdraft_limit=500):
        # TODO: store overdraft_limit, call super().__init__
        pass

    def account_type(self):
        return "Current Account"

    def deposit(self, amount):
        # TODO: validate amount > 0, then credit
        pass

    def withdraw(self, amount):
        # TODO: validate amount > 0
        # check balance - amount >= -overdraft_limit
        # debit if allowed, raise ValueError if not
        pass

    def apply_overdraft_fee(self, fee=5.00):
        # TODO: if balance < 0, charge the fee
        pass


class SavingsAccount(Account):
    def __init__(self, owner_name, initial_deposit=0, interest_rate=0.04):
        # TODO: store interest_rate, withdrawals_this_month=0, call super
        pass

    def account_type(self):
        return "Savings Account"

    def deposit(self, amount):
        # TODO
        pass

    def withdraw(self, amount):
        # TODO: max 3 withdrawals per month — raise ValueError if exceeded
        # also check sufficient funds
        pass

    def apply_interest(self):
        # TODO: add balance * (rate / 12), rounded to 2dp
        pass

    def reset_monthly_withdrawals(self):
        # TODO
        pass


class ISA(Account):
    ANNUAL_LIMIT = 20_000

    def __init__(self, owner_name, initial_deposit=0, interest_rate=0.05):
        # TODO: store interest_rate, deposited_this_year=0, call super
        pass

    def account_type(self):
        return "Cash ISA"

    def deposit(self, amount):
        # TODO: check annual limit not exceeded, then credit
        # update deposited_this_year
        pass

    def withdraw(self, amount):
        # TODO: check sufficient funds, then debit
        pass

    def apply_interest(self):
        # TODO: same as SavingsAccount
        pass

    def new_tax_year(self):
        # TODO: reset deposited_this_year to 0
        pass


class Bank:
    def __init__(self, name):
        self.__name     = name
        self.__accounts = {}

    def open_account(self, account):
        # TODO: store account keyed by account_number, print confirmation
        pass

    def get_account(self, account_number):
        # TODO: return account or raise KeyError
        pass

    def transfer(self, from_number, to_number, amount):
        # TODO: withdraw from one account, deposit to another
        pass

    def summary(self):
        # TODO: print all accounts and the total balance held across all accounts
        pass


if __name__ == "__main__":
    bank = Bank("PyBank")

    alice_current = bank.open_account(CurrentAccount("Alice", 2000))
    alice_isa     = bank.open_account(ISA("Alice", 5000))
    bob_savings   = bank.open_account(SavingsAccount("Bob", 1000, interest_rate=0.035))

    alice_current.deposit(500)
    alice_current.withdraw(200)

    try:
        alice_current.withdraw(5000)
    except ValueError as e:
        print(f"  ✗ {e}")

    bob_savings.apply_interest()
    bank.transfer(alice_current.account_number, bob_savings.account_number, 300)

    alice_current.statement()
    bank.summary()
