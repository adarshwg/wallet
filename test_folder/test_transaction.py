import datetime
import unittest
from unittest.mock import patch, MagicMock
import transaction
from transaction import Transaction

import utils.db_operations


class TestTransaction(unittest.TestCase):
    @patch('utils.db_operations.get_current_transaction_id')
    @patch('utils.db_operations.insert')
    def test__init__(self, mock_insert, mock_get_current_transaction_id):
        mock_insert.return_value = None
        mock_get_current_transaction_id.return_value = 144
        result = Transaction(100, 'ad123', 'aman123', 'misc')
        assert result.transaction_id == 144
        current = datetime.datetime.now()
        mock_insert.assert_called_once_with(100, 'ad123', 'aman123', current.month, current.year, 'misc')
        mock_get_current_transaction_id.assert_called_once()

    @patch('transaction.db_operations.get_transaction')
    def test_get_transaction_by_id(self, mocked_get_transaction_by_id):
        mocked_get_transaction_by_id.return_value = [(1, 1000, 'aman', 'ad123', 8, 2024, 'misc')]
        result = transaction.Transaction.get_transaction_by_id(1, 'aman')
        assert result == [(1, 1000, 'aman', 'ad123', 8, 2024, 'misc')]
        mocked_get_transaction_by_id.assert_called_once_with(1, 'aman')
