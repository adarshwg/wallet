from authentication import Authentication
from wallet import Wallet
from utils import db_operations
from Exceptions import LowBalanceException, UserNotFoundException, InvalidPasswordException, WalletEmptyException


class User:
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = Authentication.hash_password(password)
        db_operations.create_user(username, self.hashed_password)
        self.wallet = Wallet(username)

    @staticmethod
    def login(username, password):
        try:
            authorized = Authentication.login(username, password.encode('utf-8'))
        except UserNotFoundException:
            raise UserNotFoundException
        except InvalidPasswordException:
            raise InvalidPasswordException
        if authorized:
            return 1
        else:
            return 0

    def get_user_balance(self):
        return self.wallet.get_balance()
