import unittest
from unittest.mock import patch, MagicMock
import wallet
from wallet import Wallet


class TestWallet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet_obj = Wallet('ad123')

    @patch('wallet.db_operations.get_user_balance_from_wallet')
    def test_get_balance(self, mock_get_wallet_balance):
        mock_get_wallet_balance.return_value = 100
        result = Wallet.get_balance(self.wallet_obj)
        assert result == 100
        mock_get_wallet_balance.assert_called_once_with(self.wallet_obj.username)

    @patch('wallet.Wallet.send_amount')
    @patch('wallet.Wallet.create_transaction')
    def test_update_amount_send(self, mocked_create_transaction,
                                mocked_send_amount
                                ):
        mocked_create_transaction.return_value = None
        mocked_send_amount.return_value = None
        self.wallet_obj.update_amount(20000, 'ad123', 'aman123', 'misc')
        mocked_send_amount.assert_called_once_with(20000)
        mocked_create_transaction.assert_called_once_with(20000, 'ad123', 'aman123', 'misc')

    @patch('wallet.Wallet.receive_amount')
    @patch('wallet.Wallet.create_transaction')
    def test_update_amount_receive(self, mocked_create_transaction,
                                   mocked_receive_amount
                                   ):
        mocked_create_transaction.return_value = None
        mocked_receive_amount.return_value = None
        self.wallet_obj.update_amount(20000, 'aman123', 'ad123', 'misc')
        mocked_receive_amount.assert_called_once_with(20000)
        mocked_create_transaction.assert_called_once_with(20000, 'aman123', 'ad123', 'misc')

    @patch('wallet.db_operations.update_user_wallet_balance')
    def test_send_amount(self,mocked_update_wallet_balance):
        mocked_update_wallet_balance_return = MagicMock()
        mocked_update_wallet_balance_return.current_balance = 100

        mocked_update_wallet_balance.return_value = mocked_update_wallet_balance_return
        self.wallet_obj.send_amount(10000)
        mocked_update_wallet_balance.assert_called_once_with('ad123',-10000)

    @patch('wallet.db_operations.update_user_wallet_balance')
    def test_received_amount(self, mocked_update_wallet_balance):
        mocked_update_wallet_balance_return = MagicMock()
        mocked_update_wallet_balance_return.current_balance = 100

        mocked_update_wallet_balance.return_value = mocked_update_wallet_balance_return
        self.wallet_obj.receive_amount(10000)
        mocked_update_wallet_balance.assert_called_once_with('ad123', 10000)
