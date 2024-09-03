import unittest
from unittest.mock import patch, MagicMock
import wallet
from wallet import Wallet


class TestWallet(unittest.TestCase):
    pass
    # @classmethod
    # def setUpClass(cls):
    #     cls.wallet_obj = Wallet('adarsh123456')
    #
    # @patch('wallet.db_operations.get_user_balance_from_wallet')
    # def test_get_balance(self, mock_get_wallet_balance):
    #     mock_get_wallet_balance.return_value = 100
    #     result = Wallet.get_balance(self.wallet_obj.username)
