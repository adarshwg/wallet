from transaction_manager import TransactionManager
from utils import db_operations


class Wallet(TransactionManager):
    def __init__(self, username):
        self.username = username
        db_operations.create_table_wallets()
        db_operations.create_table_transactions()
        if db_operations.check_if_user_wallet_exists(self.username):
            self.current_balance = db_operations.get_user_balance_from_wallet(self.username)
            return

        super().__init__()
        db_operations.create_user_wallet(username)
        self.current_balance = 0

    def get_balance(self):
        return db_operations.get_user_balance_from_wallet(self.username)

    def update_amount(self, amount, sender, receiver, category):
        Wallet.create_transaction(amount, sender, receiver, category)
        if sender == self.username:
            self.__send_amount(amount)
        else:
            self.__receive_amount(amount)

    def __send_amount(self, amount):
        self.current_balance -= amount
        print(self.current_balance, amount)
        db_operations.update_user_wallet_balance(self.username, -amount)

    def __receive_amount(self, amount):
        print(self.current_balance,type(self.current_balance))
        print(amount,type(amount))
        self.current_balance += amount
        db_operations.update_user_wallet_balance(self.username, amount)

