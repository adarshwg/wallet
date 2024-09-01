from utils import db_operations
import bcrypt
import re
from Errors import UserNotFoundError, WalletEmptyError, InvalidPasswordError


class Authentication:
    def __init__(self):
        pass

    @staticmethod
    def hash_password(password):
        byte_arr = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(byte_arr, salt)
        return hashed_pass

    @staticmethod
    def check_username_format(username):
        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?!.* ).{5,}$'
        result = re.match(pattern, username)
        try :
            if result.group():
                return result.group() == username
        except AttributeError:
            return False

    @staticmethod
    def check_password_format(password):
        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{5,}$'
        result = re.match(pattern, password)
        if result:
            return result.group() == password
        else:
            return False

    def signup(self, username, password):
        user_exists = db_operations.check_if_user_exists(username)

        if user_exists:
            print('User already exists!!!')
        else:
            password = self.hash_password(password)
            db_operations.create_user(username, password)
            print(f'user with username {username} created!!')

    @staticmethod
    def match_password(username, entered_password):
        # entered_password_bytes = entered_password.encode('utf-8')
        user_password = db_operations.get_hashed_user_password(username)
        result = bcrypt.checkpw(entered_password, user_password)
        return result

    @staticmethod
    def login(username, entered_password):
        user_exists = db_operations.check_if_user_exists(username)
        if not user_exists:
            raise UserNotFoundError('User not found !!')
        else:
            if Authentication.match_password(username, entered_password):
                return 1
            else:
                raise InvalidPasswordError('Invalid password entered !')

    @staticmethod
    def check_if_username_exists(username):
        return db_operations.check_if_user_exists(username)
