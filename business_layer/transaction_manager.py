from business_layer.transaction import Transaction
from utils.db import db_operations
from datetime import datetime
from utils.Exceptions import InvalidDateException, NoRecordsException,DatabaseException


class TransactionManager:
    def __init__(self):
        pass

    @classmethod
    def create_transaction(cls, amount, sender, receiver, category):
        try:
            new_transaction = Transaction(amount, sender, receiver, category)
        except DatabaseException:
            raise DatabaseException
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
        except DatabaseException:
            raise DatabaseException

    @staticmethod
    def get_transaction_dictionary(result):
        return {
            "transaction_id": result[0],
            "amount": result[1],
            "sender": result[3],
            "receiver": result[2],
            "hours": result[8],
            "minutes": result[9],
            "day": result[7],
            "month": result[4],
            "year": result[5],
            "category": result[6]
        }

    @staticmethod
    def get_last_n_transactions(username, number=10):
        if not isinstance(number, int):
            print('Please enter valid integer !!')
            return None
        try:
            fetched_results = db_operations.get_last_n_transactions(username, number)
            result_list = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
        except Exception:
            raise DatabaseException
        return result_list

    @staticmethod
    def get_top_n_transactions(username, number=10):
        if not isinstance(number, int):
            raise ValueError('Not a number.db')
        try:
            fetched_results = db_operations.get_top_n_transactions(username, number)
            result_list = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
        except Exception:
            raise DatabaseException
        return result_list

    @staticmethod
    def get_transactions_by_month(month: int, year: int, username):
        curr_month = datetime.now().date().month
        curr_year = datetime.now().date().year
        if (month < 0 or month > 12 or year < 1900 or year > curr_year) or \
                (year == curr_year and month > curr_month):
            raise InvalidDateException('Invalid date entered!')
        try:
            fetched_results = db_operations.get_transaction_by_month(month, year, username)
            result_list = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
        except Exception:
            raise DatabaseException
        return result_list[::-1]

    @staticmethod
    def get_current_month_transactions(username):
        current_datetime = datetime.now().date()
        try:
            return (TransactionManager.get_transactions_by_month
                    (current_datetime.month, current_datetime.year, username))[::-1]
        except DatabaseException:
            raise DatabaseException

    @staticmethod
    def get_top_ten_recent_contacts(username):
        try:
            fetched_results = db_operations.get_top_ten_recent_contacts(username)
            recent_contacts = [user[0] for user in fetched_results]
            return recent_contacts[::-1]
        except DatabaseException:
            raise DatabaseException

    @staticmethod
    def get_all_transactions_for_contact(username,contact):
        try:
            fetched_results = db_operations.get_all_transactions_for_contact(username,contact)
            transactions = [TransactionManager.get_transaction_dictionary(result) for result in fetched_results]
            return transactions
        except DatabaseException:
            raise DatabaseException

