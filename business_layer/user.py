import sqlite3
from business_layer.authentication import Authentication
from business_layer.wallet import Wallet
from utils.db import db_operations
from utils.Exceptions import UserNotFoundException, InvalidMudraPinException, InvalidPasswordException, \
    WalletEmptyException, DatabaseException


class User:
    def __init__(self, username):
        self.username = username
        self.wallet = Wallet(username)

    def get_user_balance(self):
        return self.wallet.get_balance()

    @staticmethod
    def get_user_email_from_username(username):
        try:
            email_id = db_operations.get_user_email_id(username)
        except UserNotFoundException:
            raise UserNotFoundException
        except Exception:
            raise DatabaseException
        return email_id

    @staticmethod
    def change_user_password(username, new_password):
        try:
            if not Authentication.check_username_format(username):
                raise UserNotFoundException
            elif not Authentication.check_password_format(new_password):
                raise InvalidPasswordException
            print('password changed............')
            entered_password_hash = Authentication.hash_password(new_password)
            db_operations.update_user_password(username, entered_password_hash)
        except UserNotFoundException:
            raise UserNotFoundException
        except InvalidPasswordException:
            raise InvalidPasswordException
        except Exception:
            raise DatabaseException

    @staticmethod
    def change_user_mudra_pin(username, new_mudra_pin):
        try:
            if not Authentication.check_mudra_pin_format(new_mudra_pin):
                raise InvalidMudraPinException
            db_operations.update_user_mudra_pin(username, new_mudra_pin)
        except UserNotFoundException:
            raise UserNotFoundException
        except InvalidPasswordException:
            raise InvalidPasswordException
        except InvalidMudraPinException:
            raise InvalidMudraPinException
        except Exception:
            raise DatabaseException
