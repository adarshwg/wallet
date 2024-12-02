from business_layer.user import User
from business_layer.authentication import Authentication
from utils.db.create_tables import create_all_tables
from utils import input_handler
# import getpass
from datetime import datetime
from utils.db.connection import conn

auth_message = """
Choose an option :
1. Login to account
2. Sign up as user
3. Exit\n
"""

wallet_message = """
Choose an option :
1. See wallet
2. Get transaction by id
3. Get last n transactions
4. Get top n transactions
5. Get current month transactions
6. Get transactions by month
7. Sent Amount
8. Received Amount
9. Exit
"""

create_all_tables()


# def get_transaction_by_id(transaction_id, new_user):
#     result = new_user.wallet.get_transaction_by_id(transaction_id, new_user.username)
#     if not result:
#         return
#     for transaction in result:
#         transaction_id, amount, sender, receiver, month, year, category = tuple([transaction[i]
#                                                                                  for i in range(len(transaction))])
#         transaction_repr = (f'--------------------Transaction--------------------- \n'
#                             f'Amount : {amount},\t'
#                             f'Sender : {sender},\t'
#                             f'Receiver : {receiver},\t'
#                             f'Month : {month},\t'
#                             f'Year : {year},\t'
#                             f'Category : {category},\t'
#                             f'Transaction_ID :  {transaction_id}\n'
#                             f'-----------------------------------------------------\n'
#                             )
#         print(transaction_repr)
#
#
# def get_transaction_dictionary(amount, sender, receiver, category):
#     return {
#         'amount': amount,
#         'sender': sender,
#         'receiver': receiver,
#         'category': category
#     }
#
#
# def send_amount(new_user):
#     while True:
#         amount = input_handler.int_handler('Enter the amount involved : ')
#         if amount != -1:
#             break
#
#     sender = new_user.username
#     while True:
#         receiver = input_handler.username_handler('Enter the receiver : ')
#         if receiver:
#             break
#         else:
#             print('Username can contain only alpha_nums(minimum one alphabet!)')
#             continue
#     category = input('Enter the category : ')
#     return get_transaction_dictionary(amount, sender, receiver, category)
#
#
# def receive_amount(new_user):
#     while True:
#         amount = input_handler.int_handler('Enter the amount involved : ')
#         if amount != -1:
#             break
#
#     receiver = new_user.username
#     while True:
#         sender = input_handler.username_handler('Enter the sender : ')
#         if sender:
#             break
#         else:
#             print('Username can contain only alpha_nums(minimum one alphabet!)')
#             continue
#
#     category = input('Enter the category : ')
#     return get_transaction_dictionary(amount, sender, receiver, category)
#
#
# def add_transaction(new_user, new_transaction):
#     # try:
#     is_added = new_user.update_amount(
#         new_transaction['amount'],
#         new_transaction['sender'],
#         new_transaction['receiver'],
#         new_transaction['category']
#     )
#     if is_added:
#         print('Transaction has been added successfully !')
#
#
# def wallet_functionalities(new_user):
#     wallet_input = input(wallet_message)
#     if wallet_input == '1':
#         print(new_user.wallet)
#     elif wallet_input == '2':
#         while True:
#             transaction_id = input_handler.int_handler('Enter the transaction id : ')
#             if transaction_id != -1:
#                 break
#         get_transaction_by_id(transaction_id, new_user)
#     elif wallet_input == '3':
#         while True:
#             number = input_handler.int_handler('Enter the number.db of transactions (default :10) :')
#             if number != -1:
#                 break
#             else:
#                 print('Enter positive number.db only !')
#         if not number:
#             number = 10
#         list_of_transactions = new_user.wallet.get_last_n_transactions(new_user.username, number)
#         if not list_of_transactions:
#             return
#         for transaction in list_of_transactions:
#             get_transaction_by_id(transaction[0], new_user)
#         print(f'Found {len(list_of_transactions)} matching transactions !\n')
#     elif wallet_input == '4':
#         while True:
#             number = input_handler.int_handler('Enter the number.db of transactions (default :10) :')
#             if number != -1:
#                 break
#             else:
#                 print('Enter positive number.db only !')
#         if not number:
#             number = 10
#         list_of_top_transactions = new_user.wallet.get_top_n_transactions(new_user.username, number)
#         if not list_of_top_transactions:
#             return
#         for transaction in list_of_top_transactions:
#             get_transaction_by_id(transaction[0], new_user)
#         print(f'Found {len(list_of_top_transactions)} matching transactions !\n')
#     elif wallet_input == '5':
#         current_month_transactions = new_user.wallet.get_current_month_transactions(new_user.username)
#         if not current_month_transactions:
#             return
#         for transaction in current_month_transactions:
#             get_transaction_by_id(transaction[0], new_user)
#         print(f'Found {len(current_month_transactions)} matching transactions !\n')
#     elif wallet_input == '6':
#         curr_month = datetime.now().date().month
#         curr_year = datetime.now().date().year
#         while True:
#             month = input_handler.int_handler('Enter the month in number.db : ')
#             if month > -1 and 0 < month <= 12:
#                 break
#             else:
#                 print('Enter valid month which exists before !')
#         while True:
#             year = input_handler.int_handler('Enter the year : ')
#             if month > curr_month and year == curr_year:
#                 print('Cannot see transactions of the future! ')
#             if year != -1 and 1900 < year <= curr_year:
#                 break
#             else:
#                 print('Enter valid year !')
#         selected_month_transactions = new_user.wallet.get_transactions_by_month(month, year, new_user.username)
#         if not selected_month_transactions:
#             return
#         for transaction in selected_month_transactions:
#             get_transaction_by_id(transaction[0], new_user)
#     elif wallet_input == '7':
#         add_transaction(new_user, send_amount(new_user))
#         print('Updated wallet balance is : ', new_user.get_user_balance())
#     elif wallet_input == '8':
#         add_transaction(new_user, receive_amount(new_user))
#         print('Updated wallet balance is : ', new_user.get_user_balance())
#     elif wallet_input == '9':
#         return 1
#     else:
#         print('Invalid option chosen!')
#
#
# def login_function():
#     username = input('Enter your username : ')
#     # password = getpass.getpass(prompt='Enter Password: ')
#     password = input('Enter your password : ')
#     username_check = Authentication.check_username_format(username)
#     password_check = Authentication.check_password_format(password)
#     if not username_check or not password_check:
#         print('Enter valid username and password format!!')
#         return
#     value = Authentication.login(username, password)
#     if not value:
#         return
#     user_object = User(username, password)
#     call_result = wallet_functionalities(user_object)
#     while True:
#         if call_result == 1:
#             break
#         continue_in_wallet = input_handler.string_handler('Do you wish to continue? y/n :\n')
#         if continue_in_wallet.lower() == 'y':
#             call_result = wallet_functionalities(user_object)
#         elif continue_in_wallet.lower() == 'n':
#             break
#         else:
#             print('Enter y/n only :')
#
#
# def signup_function():
#     username = input('Enter your username :')
#     password = input('Enter your password :')
#     username_check = Authentication.check_username_format(username)
#     password_check = Authentication.check_password_format(password)
#     if not username_check or not password_check:
#         print('Enter valid username and password format!!')
#         return
#     if Authentication.check_if_username_exists(username):
#         print('This username already exists! ')
#         return
#     new_user = User(username, password)
#     call_result = wallet_functionalities(new_user)
#     while True:
#         if call_result == 1:
#             break
#         continue_in_wallet = input_handler.string_handler('Do you wish to continue? y/n :\n')
#         if continue_in_wallet.lower() == 'y':
#             call_result = wallet_functionalities(new_user)
#         elif continue_in_wallet.lower() == 'n':
#             break
#         else:
#             print('Enter y/n only :')
#
#
# def caller_function():
#     user_input = input(auth_message)
#     if user_input == '1':
#         login_function()
#         return 0
#     elif user_input == '2':
#         signup_function()
#         return 0
#     elif user_input == '3':
#         conn.close()
#         return 1
#     else:
#         print('Please enter valid choice! ')
#
#
# if __name__ == '__main__':
#     while True:
#         call_value = caller_function()
#         if call_value == 1:
#             break
