from transaction import Transaction
from utils import db_operations
from datetime import datetime


class TransactionManager:
    def __init__(self):
        pass

    @classmethod
    def create_transaction(cls, amount, sender, receiver, category):
        Transaction(amount, sender, receiver, category)

    @staticmethod
    def get_transaction_by_id(transaction_id, username):
        return Transaction.get_transaction_by_id(transaction_id, username)

    @staticmethod
    def get_last_n_transactions(username, number=10):
        fetched_results = db_operations.get_last_n_transactions(username, number)
        result_list = [result for result in fetched_results]
        return result_list

    @staticmethod
    def get_top_n_transactions(username, number=10):
        fetched_results = db_operations.get_top_n_transactions(username, number)
        result_list = [result for result in fetched_results]
        return result_list

    # @classmethod
    # def get_current_month_transactions(cls,username):
    #     return db_operations.get_current_month_transactions(username)
    @staticmethod
    def get_transactions_by_month(month: int, year: int, username):
        return db_operations.get_transaction_by_month(month, year, username)

    @staticmethod
    def get_current_month_transactions(username):
        current_datetime = datetime.now().date()
        return (TransactionManager.get_transactions_by_month
                (current_datetime.month, current_datetime.year, username))

    def spend_analysis(self):
        pass
        #todo 3
