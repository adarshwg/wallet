import unittest
from unittest.mock import patch, MagicMock
import utils.db_operations
from Exceptions import UserNotFoundException, WalletEmptyException


class TestDBOperations(unittest.TestCase):
    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    def test_check_if_user_exists(self, mock_cursor, mock_conn):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [('ad123', b'password')]
        mock_conn.commit.return_value = None
        result = utils.db_operations.check_if_user_exists('ad123')
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called_once_with('select * from user where username=?', ('ad123',))
        mock_cursor.fetchall.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('utils.db_operations.check_if_user_exists')
    def test_create_user_existing(self, mock_check_user_exist):
        mock_check_user_exist.return_value = True
        utils.db_operations.create_user('ad123', b'adarsh')
        mock_check_user_exist.assert_called_once_with('ad123')

    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    @patch('utils.db_operations.check_if_user_exists')
    def test_create_user_not_existing(self, mock_check_user_exist, mock_cursor, mock_conn):
        mock_check_user_exist.return_value = False
        mock_cursor.execute.return_value = None
        mock_conn.commit.return_value = None
        result = utils.db_operations.create_user('ad123', b'adarsh')
        mock_check_user_exist.assert_called_once_with('ad123')

        mock_cursor.execute.assert_called_once_with('insert into user values (?,?)', ('ad123', b'adarsh'))
        mock_conn.commit.assert_called_once()
        assert result is None

    @patch('utils.db_operations.check_if_user_exists')
    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    def test_get_hashed_user_password_valid_user(self, mock_cursor, mock_conn, mocked_check_user_exist):
        mocked_check_user_exist.return_value = True
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(b'password',)]
        mock_conn.commit.return_value = None
        result = utils.db_operations.get_hashed_user_password('ad123')
        assert result == b'password'
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called_once_with('select password from user where username=?', ('ad123',))
        mock_cursor.fetchall.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('utils.db_operations.check_if_user_exists')
    def test_get_hashed_user_password_invalid_user(self, mock_check_if_user_exists):
        mock_check_if_user_exists.return_value = False
        with self.assertRaises(UserNotFoundException):
            utils.db_operations.get_hashed_user_password('ad123')
        mock_check_if_user_exists.assert_called_once_with('ad123')

    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    def test_create_user_wallet(self, mock_cursor, mock_conn):
        mock_cursor.execute.return_value = None
        mock_conn.commit.return_value = None
        utils.db_operations.create_user_wallet('ad123')
        mock_cursor.execute.assert_called_once_with('insert into wallets values (?,0)', ('ad123',))
        mock_conn.commit.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_user_balance_from_wallet_user_exists(self, mock_cursor, ):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1000,)]
        res = utils.db_operations.get_user_balance_from_wallet('ad123')
        assert res == 1000
        mock_cursor.execute.assert_called_once_with('select amount from wallets where username=?', ('ad123',))
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_user_balance_from_wallet_user_not_exists(self, mock_cursor, ):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = []
        with self.assertRaises(UserNotFoundException):
            utils.db_operations.get_user_balance_from_wallet('ad123')

        mock_cursor.execute.assert_called_once_with('select amount from wallets where username=?', ('ad123',))
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_check_if_user_wallet_exists_true(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [('ad123', 2000)]
        result = utils.db_operations.check_if_user_wallet_exists('ad123')
        self.assertTrue(result)

    @patch('utils.db_operations.cursor')
    def test_check_if_user_wallet_exists_false(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = []
        result = utils.db_operations.check_if_user_wallet_exists('ad123')
        self.assertFalse(result)

    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    @patch('utils.db_operations.get_user_balance_from_wallet')
    def test_update_user_wallet_balance_valid(self, mock_get_user_wallet_balance,
                                              mock_cursor,
                                              mock_conn
                                              ):
        mock_get_user_wallet_balance.return_value = 1000
        mock_cursor.execute.return_value = None
        mock_conn.commit.return_value = None
        utils.db_operations.update_user_wallet_balance('ad123', 100000)
        mock_cursor.execute.assert_called_once_with('update wallets set'
                                                    ' amount= ? where username= ?',
                                                    (1000 + 100000, 'ad123'))
        mock_conn.commit.assert_called_once()

    @patch('utils.db_operations.get_user_balance_from_wallet')
    def test_update_user_wallet_balance_invalid(self, mock_get_wallet_balance):
        mock_get_wallet_balance.return_value = 0
        with self.assertRaises(WalletEmptyException):
            utils.db_operations.update_user_wallet_balance('ad123', -10000)
        mock_get_wallet_balance.assert_called_once_with('ad123')

    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    def test_insert(self, mock_cursor, mock_conn):
        mock_cursor.execute.return_value = None
        mock_conn.commit.return_value = None
        utils.db_operations.insert('a', 'b', 'c', 'd', 'e', 'f')
        mock_cursor.execute.assert_called_once_with('insert into transactions values (null,?,?,?,?,?,?)',
                                                    ('a', 'b', 'c', 'd', 'e', 'f'))
        mock_conn.commit.assert_called_once()

    @patch('utils.db_operations.conn')
    @patch('utils.db_operations.cursor')
    def test_insert_default_category(self, mock_cursor, mock_conn):
        mock_cursor.execute.return_value = None
        mock_conn.commit.return_value = None
        utils.db_operations.insert('a', 'b', 'c', 'd', 'e')
        mock_cursor.execute.assert_called_once_with('insert into transactions values (null,?,?,?,?,?,?)',
                                                    ('a', 'b', 'c', 'd', 'e', 'misc'))
        mock_conn.commit.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_transaction(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, 'a', 'b', 'c')]
        result = utils.db_operations.get_transaction(1, 'a')
        assert result == [(1, 'a', 'b', 'c')]
        mock_cursor.execute.assert_called_once_with(
            'select * from transactions where id= ? and (sender=? or receiver=?)',
            (1, 'a', 'a'))
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_current_transaction_id(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [[(1, 'a', '8', '2024')]]
        result = utils.db_operations.get_current_transaction_id()
        assert result == (1, 'a', '8', '2024')
        mock_cursor.execute.assert_called_once_with('select max(id) from transactions')
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_top_n_transactions_default(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, 'a', 'b', 'c')]
        result = utils.db_operations.get_top_n_transactions('ad123')
        assert result == [(1, 'a', 'b', 'c')]
        mock_cursor.execute.assert_called_once_with(
            'select * from transactions where (sender=? or receiver=?) order by amount desc limit ?',
            ('ad123', 'ad123', 10,))
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_top_n_transactions_with_n(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, 'a', 'b', 'c')]
        result = utils.db_operations.get_top_n_transactions('ad123', 100)
        assert result == [(1, 'a', 'b', 'c')]
        mock_cursor.execute.assert_called_once_with(
            'select * from transactions where (sender=? or receiver=?) order by amount desc limit ?',
            ('ad123', 'ad123', 100,))
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_last_n_transactions_default(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, 'a', 'b', 'c')]
        result = utils.db_operations.get_last_n_transactions('ad123')
        assert result == [(1, 'a', 'b', 'c')]
        mock_cursor.execute.assert_called_once_with(
            'select * from transactions where (sender=? or receiver=?) order by id desc limit ?',
            ('ad123', 'ad123', 10,))
        mock_cursor.fetchall.assert_called_once()

    @patch('utils.db_operations.cursor')
    def test_get_transaction_by_month(self, mock_cursor):
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, 'a', 'b', 'c')]
        result = utils.db_operations.get_transaction_by_month(1, 2023, 'ad123')
        assert result == [(1, 'a', 'b', 'c')]
        mock_cursor.execute.assert_called_once_with(
            'select * from transactions where month=? and year=? and (sender=? or receiver = ?)',
            (1, 2023, 'ad123', 'ad123'))
        mock_cursor.fetchall.assert_called_once()
