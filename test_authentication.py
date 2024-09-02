import re
import unittest
from unittest.mock import patch, MagicMock
import pytest

import authentication
from authentication import Authentication
from Errors import UserNotFoundError, InvalidPasswordError


class TestAuthentication(unittest.TestCase):

    @patch('authentication.bcrypt.hashpw')
    def test_hash_password(self, mock_hashpw):
        password = 'Secure'
        mock_hashpw.return_value = b'hashed_password'
        result = authentication.bcrypt.hashpw(password)
        mock_hashpw.assert_called_once_with(password)
        self.assertEqual(result, b'hashed_password')

    @patch('authentication.re.match')
    def test_check_username_format(self, mock_re_match):
        mock_re_object = MagicMock()
        mock_re_object.group.return_value = 'ad123'
        mock_re_match.return_value = mock_re_object
        result = Authentication.check_username_format('ad123')
        mock_re_object.group.assert_called_once()
        self.assertTrue(result)
        mock_re_match.assert_called_once_with(r'^(?=.*[0-9])(?=.*[a-z])(?!.* ).{5,}$', 'ad123')

    @patch('authentication.re.match')
    def test_check_username_format_invalid(self, mock_re_match):
        mock_match_obj = MagicMock()
        mock_match_obj.group.return_value = 'adarsh'
        mock_re_match.return_value = mock_match_obj
        result = Authentication.check_username_format('adarsh123')
        self.assertFalse(result)

    @patch('authentication.re.match')
    def test_check_password_format(self, mock_re_match):
        mock_re_object = MagicMock()
        mock_re_object.group.return_value = 'Adarsh123@'
        mock_re_match.return_value = mock_re_object

        result = Authentication.check_password_format('Adarsh123@')
        self.assertTrue(result)
        mock_re_object.group.assert_called_once()
        mock_re_match.assert_called_once_with(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{5,}$', 'Adarsh123@')

    @patch('authentication.re.match')
    def test_check_password_format_invalid(self, mock_re_match):
        mock_re_object = MagicMock()
        mock_re_object.group.return_value = 'Adarsh123@'
        mock_re_match.return_value = mock_re_object
        result = Authentication.check_password_format('Adarsh123')
        self.assertFalse(result)

    @patch('authentication.bcrypt.checkpw')
    @patch('authentication.db_operations.get_hashed_user_password')
    def test_match_password(self, mock_get_hashed_user_password, mock_checkpw):
        mock_get_hashed_user_password.return_value = b'password'
        mock_checkpw.return_value = True
        result = Authentication.match_password('adarsh', 'Adarsh@123')
        self.assertTrue(result)
        mock_get_hashed_user_password.assert_called_once_with('adarsh')
        mock_checkpw.assert_called_once_with('Adarsh@123',
                                             authentication.db_operations.get_hashed_user_password('adarsh'))

    @patch('authentication.bcrypt.checkpw')
    @patch('authentication.db_operations.get_hashed_user_password')
    def test_match_password_failed(self, mock_get_hashed_user_password, mock_checkpw):
        mock_get_hashed_user_password.return_value = b'newpassword'
        mock_checkpw.return_value = False
        result = Authentication.match_password('adarsh', 'Adarsh@123')
        self.assertFalse(result)
        mock_get_hashed_user_password.assert_called_once_with('adarsh')
        mock_checkpw.assert_called_once_with('Adarsh@123',
                                             authentication.db_operations.get_hashed_user_password('adarsh'))

    @patch('authentication.db_operations.check_if_user_exists')
    def test_login_user_not_exists(self, mock_check_user_exists):
        mock_check_user_exists.return_value = False
        with self.assertRaises(UserNotFoundError):
            Authentication.login('ad123', 'Ad123@')
        mock_check_user_exists.assert_called_once_with('ad123')

    @patch('authentication.Authentication.match_password')
    def test_login_valid_user(self, mock_match_password):
        mock_match_password.return_value = True
        result = Authentication.match_password('ad123', 'Ad123@')
        assert result == 1

    @patch('authentication.Authentication.match_password')
    def test_login_invalid_user(self, mock_match_password):
        mock_match_password.return_value = False
        with self.assertRaises(InvalidPasswordError):
            Authentication.login('ad123', 'Ad123@')
        mock_match_password.assert_called_once_with('ad123', 'Ad123@')

    @patch('authentication.db_operations.check_if_user_exists')
    def test_check_if_username_exists(self, mock_check_user_exist):
        mock_check_user_exist.return_value = True
        result = authentication.Authentication.check_if_username_exists('ad123')
        self.assertTrue(result)
        mock_check_user_exist.assert_called_once_with('ad123')
