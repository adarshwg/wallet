# import re
# import unittest
# from unittest.mock import patch, MagicMock
# import authentication
# import utils.input_handler
# import wallet
# from authentication import Authentication
# from Errors import UserNotFoundException, InvalidPasswordException
# import app
# import user
# from utils.input_handler import int_handler, string_handler
#
#
# class TestApp(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.user_obj = user.User('Adarsh123', 'Adarsh123@')
#
#     @patch('wallet.Wallet.get_transaction_by_id')
#     def test_get_transaction_by_id_not_exist(self, mocked_get_transaction):
#         mocked_get_transaction.return_value = None
#         app.get_transaction_by_id(2, self.user_obj)
#         mocked_get_transaction.assert_called_once_with(2, 'Adarsh123')
#
#     @patch('wallet.Wallet.get_transaction_by_id')
#     def test_get_transaction_by_id_exist(self, mocked_get_transaction):
#         mocked_get_transaction.return_value = [
#             (1, 1000, 'Adarsh123', 'Manish234', 9, 2024, 'miscellaneous'),
#             (2, 200, 'Aman34', 'ad123', 8, 2024, 'miscellaneous'),
#         ]
#         app.get_transaction_by_id(2, self.user_obj)
#         mocked_get_transaction.assert_called_once_with(2, 'Adarsh123')
#
#     def test_get_transaction_dictionary(self):
#         result = app.get_transaction_dictionary(1000, 'ad123', 'aman234', 'misc')
#         assert result == {
#             'amount': 1000,
#             'sender': 'ad123',
#             'receiver': 'aman234',
#             'category': 'misc'
#         }
#
#     @patch('app.get_transaction_dictionary')
#     @patch('builtins.input', return_value='misc', )
#     @patch('utils.input_handler.username_handler', return_value='aman123')
#     @patch('utils.input_handler.int_handler', return_value=10)
#     def test_send_amount_valid_username(self,
#                                         mocked_int_handler,
#                                         mocked_username_handler,
#                                         mocked_input,
#                                         mocked_get_dictionary
#                                         ):
#         mocked_get_dictionary.return_value = {
#             'amount': 10,
#             'sender': 'ad123',
#             'receiver': 'aman123',
#             'category': 'misc'
#         }
#         app.send_amount(self.user_obj)
#         mocked_input.assert_called_once_with('Enter the category : ')
#         mocked_username_handler.assert_called_once_with('Enter the receiver : ')
#         mocked_int_handler.assert_called_once_with('Enter the amount involved : ')
#         mocked_get_dictionary.assert_called_once_with(10, 'Adarsh123', 'aman123', 'misc')
#
#     @patch('app.get_transaction_dictionary')
#     @patch('builtins.input', return_value='misc', )
#     @patch('utils.input_handler.username_handler', side_effect=['','aman123'])
#     @patch('utils.input_handler.int_handler', return_value=10)
#     def test_send_amount_invalid_username(self,
#                                           mocked_int_handler,
#                                           mocked_username_handler,
#                                           mocked_input,
#                                           mocked_get_dictionary
#                                           ):
#         mocked_get_dictionary.return_value = {
#             'amount': 10,
#             'sender': 'ad123',
#             'receiver': 'aman123',
#             'category': 'misc'
#         }
#         app.send_amount(self.user_obj)
#         mocked_input.assert_called_once_with('Enter the category : ')
#         mocked_username_handler.assert_called_with('Enter the receiver : ')
#         mocked_int_handler.assert_called_once_with('Enter the amount involved : ')
#         mocked_get_dictionary.assert_called_once_with(10, 'Adarsh123', 'aman123', 'misc')
#     @patch('app.get_transaction_dictionary')
#     @patch('utils.input_handler.string_handler',return_value = 'misc')
#     @patch('utils.input_handler.username_handler',return_value = 'aman123')
#     @patch('utils.input_handler.int_handler',return_value = 100)
#
#     def test_receive_amount_valid_username(self,
#                             mocked_int_handler,
#                             mocked_username_handler,
#                             mocked_string_handler,
#                             mocked_get_transaction_dictionary
#                             ):
#         mocked_get_transaction_dictionary.return_value = {
#             'amount':100,
#             'sender':'aman123',
#             'receiver':'Adarsh123',
#             'category':'misc'
#         }
#         app.receive_amount()
#
#
#
