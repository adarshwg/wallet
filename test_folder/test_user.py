import unittest
from unittest.mock import patch

import authentication
from user import User
from wallet import Wallet
from Errors import LowBalanceException,InvalidPasswordException,UserNotFoundException


class TestUser(unittest.TestCase):
    @classmethod
    @patch('wallet.db_operations.check_if_user_wallet_exists')
    @patch('wallet.db_operations.get_user_balance_from_wallet')
    def setUpClass(cls,
                   mocked_get_balance,
                   mocked_wallet_exist
                   ):
        mocked_get_balance.return_value = 100
        mocked_wallet_exist.return_type = True
        cls.current_balance = 100
        cls.username = 'adarsh'
        cls.wallet_obj = Wallet('Aman')
        cls.user_obj = User('add123', 'add123@')

    @patch('wallet.Wallet.__init__')
    @patch('authentication.Authentication.hash_password')
    @patch('utils.db_operations.create_user')
    def test__init__(self,mock_create_user, mock_hash_password,mock_wallet):
        mock_hash_password.return_value = b'password'
        mock_create_user.return_value = None
        mock_wallet.return_value = None
        obj1 = User('testuser123','testinG@123')
        assert obj1.hashed_password == b'password'
        assert obj1.username == 'testuser123'
        mock_wallet.assert_called_once_with('testuser123')
        mock_create_user.assert_called_once_with('testuser123',b'password')
        mock_hash_password.assert_called_once_with('testinG@123')

    @patch('authentication.Authentication.login')
    def test_login_authorized(self, mocked_login):
        mocked_login.return_value = True
        result = User.login('ad124', 'ad123@AA')
        self.assertTrue(result)
        mocked_login.assert_called_once_with('ad124', b'ad123@AA')

    @patch('authentication.Authentication.login')
    def test_login_user_not_found(self, mocked_login):
        mocked_login.side_effect = UserNotFoundException('User not found!')
        with self.assertRaises(UserNotFoundException):
            authentication.Authentication.login('adarsh123', 'Adarsh123@')
        mocked_login.assert_called_once_with('adarsh123', 'Adarsh123@')

    @patch('authentication.Authentication.login')
    def test_login_invalid_password(self, mocked_login):
        mocked_login.side_effect = InvalidPasswordException('Invalid password entered!')
        with self.assertRaises(InvalidPasswordException):
            authentication.Authentication.login('adarsh123', 'Adarsh123@')
        mocked_login.assert_called_once_with('adarsh123', 'Adarsh123@')


    @patch('wallet.Wallet.update_amount')
    def test_update_amount(self, mocked_update_amount):
        mocked_update_amount.return_value = None
        self.wallet_obj.update_amount(200, 'ad123', 'nikhil123', 'misc')
        mocked_update_amount.assert_called_once_with(200, 'ad123', 'nikhil123', 'misc')

    @patch('wallet.Wallet.update_amount')
    def test_update_amount_low_balance(self, mocked_update_amount):
        mocked_update_amount.side_effect = LowBalanceException('Low')
        with self.assertRaises(LowBalanceException):
            self.wallet_obj.update_amount(200, 'ad123', 'nikhil123', 'misc')
        mocked_update_amount.assert_called_once_with(200, 'ad123', 'nikhil123', 'misc')

    @patch('user.Wallet.get_balance')
    def test_get_user_balance(self, mocked_get_balance):
        mocked_get_balance.return_value = 100
        result = self.user_obj.get_user_balance()
        assert result == 100
        mocked_get_balance.assert_called_once()
