import re
import unittest
from unittest.mock import patch, MagicMock
import authentication
from authentication import Authentication
from Errors import UserNotFoundError, InvalidPasswordError


class TestAuthentication(unittest.TestCase) :
    @patch('authentication.bcrypt.hashpw')
    def test_hash_password (self, mock_hashpw) :
        password = 'Secure'
        mock_hashpw.return_value = b'hashed_password'
        result = authentication.bcrypt.hashpw(password)
        mock_hashpw.assert_called_once_with(password)
        self.assertEqual(result,b'hashed_password')

    @patch('authentication.re.match.group')
    @patch('authentication.re.match')
    def test_check_username_format(self, mock_match):
        username = 'adarsh123'
        pattern = r'[a-z]'
        mock_match_result = MagicMock(pattern, username)






