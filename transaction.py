from utils import db_operations
from datetime import datetime
from Exceptions import NoRecordsException


class Transaction:
    def __init__(self, amount, sender, receiver, category='misc', ):
        self.transaction_id = db_operations.get_current_transaction_id()
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        current_datetime = datetime.now().date()
        self.category = category
        self.day = current_datetime.day
        self.month = current_datetime.month
        self.year = current_datetime.year
        db_operations.insert(amount, sender, receiver, self.month, self.year, category)

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
        if not transaction:
            raise NoRecordsException('NO records found with this ID')
        return transaction
