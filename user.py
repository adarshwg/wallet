from authentication import Authentication
from wallet import Wallet
from utils import db_operations
from Errors import LowBalanceException, UserNotFoundException, InvalidPasswordException, WalletEmptyException


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
            print('User was not found!')
            return 0
        except InvalidPasswordException:
            print('Invalid password has been entered! ')
            return 0
        if authorized:
            return 1
        else:
            return 0

    def update_amount(self, amount, sender, receiver, category):
        try:
            self.wallet.update_amount(amount, sender, receiver, category)
        except LowBalanceException:
            print('User Balance is low for the transaction !!')
            return 0
        except WalletEmptyException:
            print('User wallet is empty! Please top-up')
            return 0
        except OverflowError:
            print('Too large value for the transaction !')
            return 0

    def get_user_balance(self):
        return self.wallet.get_balance()
