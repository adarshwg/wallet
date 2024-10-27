import sqlite3
from business_layer.authentication import Authentication
from business_layer.wallet import Wallet
from utils.db import db_operations
from utils.Exceptions import UserNotFoundException, InvalidPasswordException, WalletEmptyException,DatabaseException


class User:
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = Authentication.hash_password(password)
        try:
            db_operations.create_user(username, self.hashed_password)
        except sqlite3.OperationalError:
            raise DatabaseException
        self.wallet = Wallet(username)

    @staticmethod
    def login(username, password):
        try:
            authorized = Authentication.login(username, password.encode('utf-8'))
        except UserNotFoundException:
            raise UserNotFoundException
        except InvalidPasswordException:
            raise InvalidPasswordException
        except DatabaseException:
            raise DatabaseException
        if authorized:
            return 1
        else:
            return 0

    def get_user_balance(self):
        return self.wallet.get_balance()
