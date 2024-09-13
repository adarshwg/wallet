import unittest
from unittest.mock import patch, MagicMock

import transaction_manager
import wallet
from wallet import Wallet


class TestWallet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet_obj = Wallet('ad123')
        cls.wallet_obj.receive_amount(1000000)

    @patch('wallet.db_operations.get_user_balance_from_wallet')
    @patch('wallet.db_operations.check_if_user_wallet_exists')
    def test__init__user_wallet_exists(self, mock_check_wallet_exists, mock_get_wallet_balance):
        mock_check_wallet_exists.return_value = True
        mock_get_wallet_balance.return_value = 144
        test_wallet = Wallet('ad123')
        assert test_wallet.current_balance == 144
        assert test_wallet.username == 'ad123'
        mock_check_wallet_exists.assert_called_once_with(test_wallet.username)
        mock_get_wallet_balance.assert_called_once_with(test_wallet.username)

    @patch('transaction_manager.TransactionManager.__init__')
    @patch('wallet.db_operations.create_user_wallet')
    @patch('wallet.db_operations.check_if_user_wallet_exists')
    def test__init__user_wallet_not_exists(self, mock_check_wallet_exists, mock_create_wallet,
                                           mock_transaction_manager):
        mock_check_wallet_exists.return_value = False
        mock_create_wallet.return_value = None
        mock_transaction_manager.return_value = None
        test_wallet = Wallet('aman96')
        assert test_wallet.username == 'aman96'
        assert test_wallet.current_balance == 0
        mock_check_wallet_exists.assert_called_once_with('aman96')
        mock_create_wallet.assert_called_once_with('aman96')
        mock_transaction_manager.assert_called_once()

    def test__repr__(self):
        result = self.wallet_obj.__repr__()
        assert result == (f'----------------------\n'
                          f'Username : {self.wallet_obj.username}\n'
                          f'Current Balance : {self.wallet_obj.current_balance}\n'
                          f'----------------------\n'
                          )

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
    def test_send_amount(self, mocked_update_wallet_balance):
        mocked_update_wallet_balance_return = MagicMock()
        mocked_update_wallet_balance_return.current_balance = 100

        mocked_update_wallet_balance.return_value = mocked_update_wallet_balance_return
        self.wallet_obj.send_amount(10000)
        mocked_update_wallet_balance.assert_called_once_with('ad123', -10000)

    @patch('wallet.db_operations.update_user_wallet_balance')
    def test_received_amount(self, mocked_update_wallet_balance):
        mocked_update_wallet_balance_return = MagicMock()
        mocked_update_wallet_balance_return.current_balance = 100

        mocked_update_wallet_balance.return_value = mocked_update_wallet_balance_return
        self.wallet_obj.receive_amount(10000)
        mocked_update_wallet_balance.assert_called_once_with('ad123', 10000)
