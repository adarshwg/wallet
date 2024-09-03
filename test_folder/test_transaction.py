import unittest
from unittest.mock import patch, MagicMock
import transaction


class TestTransaction(unittest.TestCase):
    @patch('transaction.db_operations.get_transaction')
    def test_get_transaction_by_id(self, mocked_get_transaction_by_id):
        mocked_get_transaction_by_id.return_value = [(1, 1000, 'aman', 'ad123', 8, 2024, 'misc')]
        result = transaction.Transaction.get_transaction_by_id(1, 'aman')
        assert result == [(1, 1000, 'aman', 'ad123', 8, 2024, 'misc')]
        mocked_get_transaction_by_id.assert_called_once_with(1, 'aman')
