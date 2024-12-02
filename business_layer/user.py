import sqlite3
from business_layer.authentication import Authentication
from business_layer.wallet import Wallet
from utils.db import db_operations
from utils.Exceptions import UserNotFoundException, InvalidPasswordException, WalletEmptyException,DatabaseException


class User:
    def __init__(self, username):
        self.username = username
        self.wallet = Wallet(username)

    # @staticmethod
    # def login(username, password):
    #     try:
    #         authorized = Authentication.login(username, password.encode('utf-8'))
    #     except UserNotFoundException:
    #         raise UserNotFoundException
    #     except InvalidPasswordException:
    #         raise InvalidPasswordException
    #     except DatabaseException:
    #         raise DatabaseException
    #     if authorized:
    #         return 1
    #     else:
    #         return 0
    #
    # @staticmethod
    # def signup(username,password,email,mudra_pin):

    def get_user_balance(self):
        return self.wallet.get_balance()
