from transaction import Transaction
from utils import db_operations
from datetime import datetime
from Exceptions import InvalidDateException, NoRecordsException


class TransactionManager:
    def __init__(self):
        pass

    @classmethod
    def create_transaction(cls, amount, sender, receiver, category):
        new_transaction = Transaction(amount, sender, receiver, category)
        print('Transaction has been added successfully! ')
        return new_transaction

    @staticmethod
    def get_transaction_by_id(transaction_id, username):
        try:
            return TransactionManager.get_transaction_dictionary(
                Transaction.get_transaction_by_id(transaction_id, username)[0])
        except OverflowError:
            raise OverflowError('Too large value entered!!')
        except NoRecordsException:
            raise NoRecordsException('No transaction found with this id')

    @staticmethod
    def get_transaction_dictionary(result):
        return {
            "transaction_id": result[0],
            "amount": result[1],
            "sender": result[2],
            "receiver": result[3],
            "month": result[4],
            "year": result[5],
            "category": result[6]
        }

    @staticmethod
    def get_last_n_transactions(username, number=10):
        if not isinstance(number, int):
            print('Please enter valid integer !!')
            return None
        fetched_results = db_operations.get_last_n_transactions(username, number)
        result_list = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
        if not result_list:
            raise NoRecordsException('No records were found !')
        return result_list

    @staticmethod
    def get_top_n_transactions(username, number=10):
        if not isinstance(number, int):
            raise ValueError('Not a number')
        fetched_results = db_operations.get_top_n_transactions(username, number)
        result_list = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
        if not result_list:
            raise NoRecordsException('No records were found !')
        return result_list

    @staticmethod
    def get_transactions_by_month(month: int, year: int, username):
        curr_month = datetime.now().date().month
        curr_year = datetime.now().date().year
        if (month < 0 or month > 12 or year < 1900 or year > curr_year) or \
                (year == curr_year and month > curr_month):
            raise InvalidDateException('Invalid date entered!')
        fetched_results = db_operations.get_transaction_by_month(month, year, username)
        result_list = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
        if not result_list:
            raise NoRecordsException('No records were found !')
        return result_list

    @staticmethod
    def get_current_month_transactions(username):
        current_datetime = datetime.now().date()
        return (TransactionManager.get_transactions_by_month
                (current_datetime.month, current_datetime.year, username))
