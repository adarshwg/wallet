import unittest
from unittest.mock import patch, MagicMock

import authentication
import wallet
from user import User
from wallet import Wallet
from authentication import Authentication


class TestUser(unittest.TestCase):
    @classmethod
    @patch('wallet.db_operations.create_user_wallet')
    @patch('wallet.db_operations.create_table_wallets')
    @patch('wallet.db_operations.create_table_transactions')
    @patch('wallet.db_operations.check_if_user_wallet_exists')
    @patch('wallet.db_operations.get_user_balance_from_wallet')


    def setUpClass(cls,
                   mocked_get_balance,
                   mocked_wallet_exist,
                   mocked_create_table_transactions,
                   mocked_create_table_wallets,
                   mocked_create_user_wallet
                   ):
        mocked_get_balance.return_value = 100
        mocked_wallet_exist.return_type = True
        mocked_create_table_transactions.return_type = None
        mocked_create_table_wallets.return_type = None
        mocked_create_user_wallet.return_type = None
        cls.current_balance = 100
        cls.username='adarsh'
        cls.wallet_obj = Wallet('Aman')

    @patch('authentication.Authentication.login')
    def test_login_unauthorized(self, mocked_login):
        mocked_login.return_value = False
        result = User.login('adarsh123', 'Adarsh123@')
        self.assertFalse(result)

    @patch('authentication.db_operations.create_user')
    @patch('authentication.Authentication.login')
    def test_login_authorized(self, mocked_login, mocked_create_user):
        mocked_login.return_value = True
        mocked_create_user.return_value = None
        result = User.login('ad124', 'ad123@AA')
        self.assertTrue(result)
        mocked_login.assert_called_once_with('ad124',b'ad123@AA')
        mocked_create_user.assert_called_once()

    @patch('wallet.Wallet.update_amount')
    def test_update_amount(self,mocked_update_amount):
        mocked_update_amount.return_value = None
        self.wallet_obj.update_amount(200,'ad123','nikhil123','misc')
        mocked_update_amount.assert_called_once_with(200,'ad123','nikhil123','misc')

    @patch('wallet.Wallet.get_balance')
    def test_get_user_balance(self,mock_get_balance):
        mock_get_balance.return_value = 100
        result = Wallet.get_balance(self.wallet_obj)
        assert result == 100
        mock_get_balance.assert_called_once()


