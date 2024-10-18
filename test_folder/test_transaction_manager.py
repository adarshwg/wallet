import datetime
import unittest
from unittest.mock import patch
import transaction_manager
from transaction_manager import TransactionManager


class TestTransactionManager(unittest.TestCase):
    def test__init__(self):
        t = TransactionManager()
        assert isinstance(t,TransactionManager)

    @patch('transaction.Transaction.get_transaction_by_id')
    def test_get_transaction_by_id(self, mocked_get_transaction):
        mocked_get_transaction.return_value = [(122, 10000, 'sender', 'receiver', 8, 2024, 'misc')]
        result = transaction_manager.TransactionManager.get_transaction_by_id(122, 'sender')
        assert result == [(122, 10000, 'sender', 'receiver', 8, 2024, 'misc')]

    @patch('transaction.Transaction.get_transaction_by_id')
    def test_get_transaction_by_id_overflow(self, mocked_get_transaction):
        mocked_get_transaction.side_effect = OverflowError
        result = transaction_manager.TransactionManager.get_transaction_by_id(122, 'sender')
        assert result is None

    @patch('transaction_manager.Transaction')
    def test_create_transaction(self, mock_transaction):
        TransactionManager.create_transaction(100, 'Alice', 'Bob', 'Utilities')
        mock_transaction.assert_called_once_with(100, 'Alice', 'Bob', 'Utilities')

    @patch('utils.db_operations.get_last_n_transactions')
    def test_get_last_n_transactions(self, mock_get_last_n_transactions):
        mock_get_last_n_transactions.return_value = [
            {'id': 1, 'amount': 100},
            {'id': 2, 'amount': 200}
        ]
        result = TransactionManager.get_last_n_transactions('Alice', 2)
        self.assertEqual(result[0]['amount'], 100)
        mock_get_last_n_transactions.assert_called_once_with('Alice', 2)

    @patch('utils.db_operations.get_last_n_transactions')
    def test_get_last_n_transactions_no_result(self, mock_get_last_n_transactions):
        mock_get_last_n_transactions.return_value = []
        result = TransactionManager.get_last_n_transactions('Alice', 2)
        assert result == []
        mock_get_last_n_transactions.assert_called_once_with('Alice', 2)

    @patch('transaction_manager.db_operations.get_top_n_transactions')
    def test_get_top_n_transactions(self, mock_get_top_n_transactions):
        mock_get_top_n_transactions.return_value = [
            {'id': 1, 'amount': 500},
            {'id': 2, 'amount': 400}
        ]
        result = TransactionManager.get_top_n_transactions('Alice', 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['amount'], 500)
        mock_get_top_n_transactions.assert_called_once_with('Alice', 2)

    @patch('transaction_manager.db_operations.get_top_n_transactions')
    def test_get_top_n_transactions_no_result(self, mock_get_top_n_transactions):
        mock_get_top_n_transactions.return_value = []
        result = TransactionManager.get_top_n_transactions('Alice', 2)
        assert result == []
        mock_get_top_n_transactions.assert_called_once_with('Alice', 2)

    @patch('transaction_manager.TransactionManager.get_transactions_by_month')
    def test_get_current_month_transactions(self, mock_get_transactions_by_month):
        mock_get_transactions_by_month.return_value = [
            {'id': 1, 'amount': 100}
        ]
        result = TransactionManager.get_current_month_transactions('ad123')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['amount'], 100)
        mock_get_transactions_by_month.assert_called_once_with(datetime.datetime.now().month,
                                                               datetime.datetime.now().year, 'ad123')

    @patch('transaction_manager.db_operations.get_transaction_by_month')
    def test_get_transactions_by_month(self, mock_get_transaction_by_month):
        mock_get_transaction_by_month.return_value = [
            {'id': 1, 'amount': 100}
        ]
        result = TransactionManager.get_transactions_by_month(8, 2024, 'Alice')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['amount'], 100)
        mock_get_transaction_by_month.assert_called_once_with(8, 2024, 'Alice')

    @patch('transaction_manager.db_operations.get_transaction_by_month')
    def test_get_transactions_by_month_no_result(self, mock_get_transaction_by_month):
        mock_get_transaction_by_month.return_value = []
        result = TransactionManager.get_transactions_by_month(8, 2024, 'Alice')
        assert result is None


if __name__ == '__main__':
    unittest.main()
