class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class Bank:
    def __init__(self):
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_enabled = True
        self.transaction_history = []

    def get_total_balance(self):
        return self.total_balance

    def get_total_loan_amount(self):
        return self.total_loan_amount

    def enable_loan(self):
        self.loan_enabled = True

    def disable_loan(self):
        self.loan_enabled = False

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)


class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, initial_deposit):
        user = User(name)
        if user.create_account(initial_deposit):
            self.bank.total_balance += initial_deposit
            return user
        return None

    def get_total_balance(self):
        return self.bank.get_total_balance()

    def get_total_loan_amount(self):
        return self.bank.get_total_loan_amount()

    def enable_loan_feature(self):
        self.bank.enable_loan()

    def disable_loan_feature(self):
        self.bank.disable_loan()

    def get_transaction_history(self):
        return self.bank.transaction_history


class User:
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.loan_limit = 0
        self.transaction_history = []

    def create_account(self, initial_deposit):
        if initial_deposit > 0:
            self.balance = initial_deposit
            self.loan_limit = initial_deposit * 2
            return True
        return False

    def deposit(self, bank, amount):
        if amount > 0:
            self.balance += amount
            bank.total_balance += amount
            self.loan_limit = self.balance * 2
            transaction = Transaction(self.name, self.name, amount)
            self.transaction_history.append(transaction)
            return True
        return False

    def withdraw(self, bank, amount):
        if amount > 0 and amount <= self.balance and amount <= bank.total_balance:
            self.balance -= amount
            bank.total_balance -= amount
            transaction = Transaction(self.name, self.name, -amount)
            self.transaction_history.append(transaction)
            return True
        elif amount > bank.total_balance:
            print("Bank is bankrupt. Unable to withdraw.")
        return False

    def transfer(self, recipient, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            transaction = Transaction(self.name, recipient.name, amount)
            self.transaction_history.append(transaction)
            recipient.transaction_history.append(transaction)
            return True
        return False

    def check_balance(self):
        return self.balance

    def take_loan(self, bank, amount):
        if bank.loan_enabled and amount <= self.loan_limit and amount > 0 and amount <= bank.total_balance:
            self.balance += amount
            bank.total_loan_amount += amount
            bank.total_balance -= amount
            transaction = Transaction(self.name, self.name, amount)
            self.transaction_history.append(transaction)
            bank.add_transaction(transaction)
            return True
        return False

    def get_transaction_history(self):
        return self.transaction_history


bank = Bank()

admin = Admin(bank)

Hazrat = admin.create_account('Hazrat', 500)

Minhaz = admin.create_account('Minhaz', 100)

Hazrat.deposit(bank, 10000)

print(Hazrat.check_balance())
print(Minhaz.check_balance())

Hazrat.withdraw(bank, 1000)
Hazrat.transfer(Minhaz, 500)

admin.enable_loan_feature()

Hazrat.take_loan(bank, 100)

print(Hazrat.check_balance())

print(admin.get_total_loan_amount())
print(admin.get_total_balance())

transaction_history = Hazrat.get_transaction_history()
for transaction in transaction_history:
    print(
        f"Sender: {transaction.sender}, Receiver: {transaction.receiver}, Amount: {transaction.amount}")
