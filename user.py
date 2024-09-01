from authentication import Authentication
from wallet import Wallet
from utils import db_operations


class NotAuthenticatedError(Exception):
    pass


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.hashed_password = Authentication.hash_password(password)
        db_operations.create_user(username,self.hashed_password)
        self.wallet = Wallet(username)

    @staticmethod
    def login(username,password):
        authorized = Authentication.login(username, password.encode('utf-8'))
        if authorized:
            new_user = User(username,password)
            new_user.wallet = Wallet(new_user.username)
            return True
        else:
            return False

    # def get_user_wallet(self):
    #     if self.login == 1:
    #         return self.wallet
    #     else:
    #         raise NotAuthenticatedError('User not authenticated!')

    def update_amount(self, amount, sender, receiver, category):
        # if self.login == 1:
        self.wallet.update_amount(amount, sender, receiver, category)

    def get_user_balance(self):
        # if self.login == 1:
        return self.wallet.get_balance()


