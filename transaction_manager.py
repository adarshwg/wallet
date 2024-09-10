from transaction import Transaction
from utils import db_operations
from datetime import datetime


class TransactionManager:
    def __init__(self):
        pass

    @classmethod
    def create_transaction(cls, amount, sender, receiver, category):
        new_transaction = Transaction(amount, sender, receiver, category)
        print('Transaction has been added successfully! ')
        print(new_transaction)


    @staticmethod
    def get_transaction_by_id(transaction_id, username):
        try:
            return Transaction.get_transaction_by_id(transaction_id, username)
        except OverflowError:
            print('Tooo large value!!!')
            return None

    @staticmethod
    def get_last_n_transactions(username, number=10):
        if not isinstance(number,int):
            print('Please enter valid integer !!')
            return None
        fetched_results = db_operations.get_last_n_transactions(username, number)
        result_list = [result for result in fetched_results]
        if not result_list:
            print('No records found!')
        return result_list

    @staticmethod
    def get_top_n_transactions(username, number=10):
        if not isinstance(number,int):
            print('Please enter valid integer !!')
            return None
        fetched_results = db_operations.get_top_n_transactions(username, number)
        result_list = [result for result in fetched_results]
        if not result_list:
            print('No records found!')
        return result_list

    @staticmethod
    def get_transactions_by_month(month: int, year: int, username):
        transaction_list = db_operations.get_transaction_by_month(month, year, username)
        if not transaction_list:
            print('No records found for the specified time!')
            return
        return transaction_list

    @staticmethod
    def get_current_month_transactions(username):
        current_datetime = datetime.now().date()
        return (TransactionManager.get_transactions_by_month
                (current_datetime.month, current_datetime.year, username))

