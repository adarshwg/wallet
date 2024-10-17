from transaction_manager import TransactionManager
from utils import db_operations
from Exceptions import (WalletEmptyException, NotAuthorizedException,
                        SelfTransferException, LowBalanceException,
                        InvalidAmountException, DatabaseException)


class Wallet(TransactionManager):
    def __init__(self, username):
        self.username = username
        try:
            if db_operations.check_if_user_wallet_exists(self.username):
                self.current_balance = db_operations.get_user_balance_from_wallet(self.username)
                return
            super().__init__()
            db_operations.create_user_wallet(username)
        except Exception:
            raise DatabaseException
        self.current_balance = 0

    def __repr__(self):
        return (f'----------------------\n'
                f'Username : {self.username}\n'
                f'Current Balance : {self.current_balance}\n'
                f'----------------------\n'
                )

    def get_balance(self):
        try:
            return db_operations.get_user_balance_from_wallet(self.username)
        except Exception:
            raise DatabaseException

    def send_amount(self, receiver, amount, category='misc'):
        if self.username == receiver:
            raise SelfTransferException('Cannot transfer to the same account wallet! ')
        if self.get_balance() <= 0:
            raise WalletEmptyException('User wallet is empty!!')
        elif self.get_balance() < amount:
            raise LowBalanceException('Your wallet balance is low for the transaction!')
        if amount <= 0:
            raise InvalidAmountException
        self.current_balance -= amount
        try:
            db_operations.update_user_wallet_balance(self.username, -amount)
            new_transaction = Wallet.create_transaction(amount, self.username, receiver, category)
        except Exception:
            raise DatabaseException
        return new_transaction

    def receive_amount(self, sender, amount, category='misc'):
        if self.username == sender:
            raise SelfTransferException('Cannot transfer to the same account wallet!')
        if amount <= 0:
            raise InvalidAmountException
        self.current_balance += amount
        try:
            db_operations.update_user_wallet_balance(self.username, amount)
            new_transaction = Wallet.create_transaction(amount, sender, self.username, category)
        except Exception:
            raise DatabaseException
        return new_transaction
