from transaction import Transaction
from utils import db_operations


class TransactionManager:
    def __init__(self):
        pass

    @classmethod
    def create_transaction(cls, amount, sender, receiver, category):
        Transaction(amount, sender, receiver, category)

    @staticmethod
    def get_transaction_by_id(transaction_id):
        Transaction.get_transaction_by_id(transaction_id)

    @staticmethod
    def get_last_n_transactions(number=10):
        fetched_results = db_operations.get_last_n_transactions(number)
        result_list = [result for result in fetched_results]
        return result_list

    @staticmethod
    def get_top_n_transactions(number=10):
        fetched_results = db_operations.get_top_n_transactions(number)
        result_list = [result for result in fetched_results]
        return result_list

    def get_current_month_transactions(self):
        pass
        #todo 2

    def spend_analysis(self):
        pass
        #todo 3



