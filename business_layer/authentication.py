from utils.db import db_operations
import bcrypt
import re
from utils.Exceptions import UserAlreadyExistsException, UserNotFoundException, InvalidPasswordException, \
    DatabaseException


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
        try:
            matched_string = result.group()
            if matched_string:
                return matched_string == username
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

    @staticmethod
    def match_password(username, entered_password):
        try:
            user_password = db_operations.get_hashed_user_password(username)
        except Exception:
            raise DatabaseException
        result = bcrypt.checkpw(entered_password, user_password)
        return result

    @staticmethod
    def match_mudra_pin(username, entered_mudra_pin):
        try:
            email_id = db_operations.get_user_email_id(username)
            user_mudra_pin = db_operations.get_user_mudra_pin(email_id)
            return user_mudra_pin == entered_mudra_pin
        except Exception as err:
            #todo
            raise err

    @staticmethod
    def login(username, entered_password, entered_mudra_pin):
        try:
            user_exists = db_operations.check_if_user_exists(username)
        except Exception:
            raise DatabaseException
        if not user_exists:
            raise UserNotFoundException('User not found !!')
        else:
            try:
                if Authentication.match_password(username, entered_password) \
                        and Authentication.match_mudra_pin(username, entered_mudra_pin):
                    return 1
                else:
                    raise InvalidPasswordException('Invalid password entered !')
            except DatabaseException:
                raise DatabaseException

    @staticmethod
    def signup(entered_username, entered_password, entered_email, mudra_pin):
        try:
            user_exists = Authentication.check_if_user_exists(entered_username)
            email_exists = Authentication.check_if_user_email_exists(entered_email)
            hashed_password = Authentication.hash_password(entered_password)
        except Exception:
            raise DatabaseException
        if user_exists:
            raise UserAlreadyExistsException
        elif email_exists:
            #todo
            raise Exception
        else:
            try:
                db_operations.create_user(entered_username, hashed_password, entered_email, mudra_pin)
            except Exception:
                raise DatabaseException

    @staticmethod
    def check_if_user_email_exists(email_id):
        try:
            return db_operations.check_if_user_email_exists(email_id)
        except Exception:
            raise DatabaseException

    @staticmethod
    def check_if_user_exists(username):
        try:
            return db_operations.check_if_user_exists(username)
        except Exception:
            raise DatabaseException

    @staticmethod
    def check_username_and_password_format(username, password):
        if not Authentication.check_username_format(username) or \
                not Authentication.check_password_format(password):
            return False
        return True
