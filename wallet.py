from transaction_manager import TransactionManager
from utils import db_operations
from Errors import WalletEmptyException, NotAuthorizedException, SelfTransferException, LowBalanceException


class Wallet(TransactionManager):
    def __init__(self, username):
        self.username = username
        if db_operations.check_if_user_wallet_exists(self.username):
            self.current_balance = db_operations.get_user_balance_from_wallet(self.username)
            return

        super().__init__()
        db_operations.create_user_wallet(username)
        self.current_balance = 0

    def __repr__(self):
        return (f'----------------------\n'
                f'Username : {self.username}\n'
                f'Current Balance : {self.current_balance}\n'
                f'----------------------\n'
                )

    def get_balance(self):
        return db_operations.get_user_balance_from_wallet(self.username)

    def update_amount(self, amount, sender, receiver, category):
        if sender == receiver:
            raise SelfTransferException('Cannot transfer to the same account wallet! ')
        if sender != self.username and receiver != self.username:
            raise NotAuthorizedException('Can only add your own transactions!')
        if sender == self.username:
            if self.get_balance() <= 0:
                raise WalletEmptyException('User wallet is empty!!')
            elif self.get_balance() < amount:
                raise LowBalanceException('Your wallet balance is low for the transaction! ')
            self.send_amount(amount)
        elif receiver == self.username:
            self.receive_amount(amount)
        Wallet.create_transaction(amount, sender, receiver, category)

    def send_amount(self, amount):
        self.current_balance -= amount
        db_operations.update_user_wallet_balance(self.username, -amount)

    def receive_amount(self, amount):
        self.current_balance += amount
        db_operations.update_user_wallet_balance(self.username, amount)
