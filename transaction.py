from utils import db_operations
from datetime import datetime


class Transaction:
    def __init__(self, amount, sender, receiver, category='misc', ):
        current_datetime = datetime.now().date()
        self.year = current_datetime.year
        self.month = current_datetime.month
        self.day = current_datetime.day
        db_operations.insert(amount, sender, receiver, self.month, self.year, category)
        self.transaction_id = db_operations.get_current_transaction_id()
        self.amount = amount
        self.receiver = receiver
        self.sender = sender
        self.category = category

    def __repr__(self):
        transaction_repr = (f'--------------------------\n'
                            f'Amount : {self.amount}\n'
                            f'Sender : {self.sender}\n'
                            f'Receiver : {self.receiver}\n'
                            f'Category : {self.category}\n'
                            f'Transaction_ID : {self.transaction_id}\n'
                            f'------------------------------\n'
                            )
        return transaction_repr

    @staticmethod
    def get_transaction_by_id(transaction_id, username):
        transaction = db_operations.get_transaction(transaction_id, username)
        if not transaction :
            print('No transaction with this ID!')
        return transaction
