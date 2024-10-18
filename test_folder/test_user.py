import unittest
from unittest.mock import patch
from user import User
from wallet import Wallet
from Exceptions import LowBalanceException,InvalidPasswordException,UserNotFoundException,WalletEmptyException


class TestUser(unittest.TestCase)   :
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
    def test_login_unauthorized(self, mocked_login):
        mocked_login.return_value = False
        result = User.login('ad124', 'ad123@AA')
        self.assertFalse(result)
        mocked_login.assert_called_once_with('ad124', b'ad123@AA')

    @patch('authentication.Authentication.login')
    def test_login_user_not_found(self,mocked_login):
        mocked_login.side_effect = UserNotFoundException
        result = User.login('add123','add123@')
        assert result == 0
        mocked_login.assert_called_once_with('add123',b'add123@')

    @patch('authentication.Authentication.login')
    def test_login_invalid_password(self, mocked_login):
        mocked_login.side_effect = InvalidPasswordException
        result = User.login('adarsh123', 'Adarsh123@')
        assert result == 0
        mocked_login.assert_called_once_with('adarsh123', b'Adarsh123@')


    @patch('wallet.Wallet.update_amount')
    def test_update_amount(self, mocked_update_amount):
        mocked_update_amount.return_value = None
        self.wallet_obj.update_amount(200, 'ad123', 'nikhil123', 'misc')
        mocked_update_amount.assert_called_once_with(200, 'ad123', 'nikhil123', 'misc')

    @patch('wallet.Wallet.update_amount')
    def test_update_amount_low_balance(self, mocked_update_amount):
        mocked_update_amount.side_effect = LowBalanceException('Low')
        result = self.user_obj.update_amount(200, 'ad123', 'nikhil123', 'misc')
        assert result == 0
        mocked_update_amount.assert_called_once_with(200, 'ad123', 'nikhil123', 'misc')

    @patch('wallet.Wallet.update_amount')
    def test_update_amount_wallet_empty(self, mocked_update_amount):
        mocked_update_amount.side_effect = WalletEmptyException('Low')
        result = self.user_obj.update_amount(200, 'ad123', 'nikhil123', 'misc')
        assert result == 0
        mocked_update_amount.assert_called_once_with(200, 'ad123', 'nikhil123', 'misc')

    @patch('wallet.Wallet.update_amount')
    def test_update_amount_overflow(self, mocked_update_amount):
        mocked_update_amount.side_effect = OverflowError('Low')
        result = self.user_obj.update_amount(200, 'ad123', 'nikhil123', 'misc')
        assert result == 0
        mocked_update_amount.assert_called_once_with(200, 'ad123', 'nikhil123', 'misc')


    @patch('user.Wallet.get_balance')
    def test_get_user_balance(self, mocked_get_balance):
        mocked_get_balance.return_value = 100
        result = self.user_obj.get_user_balance()
        assert result == 100
        mocked_get_balance.assert_called_once()
