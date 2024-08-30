# API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciO'\
#             'iJIUzUxMiIsImtpZCI6IjI4YTMx'\
#             'OGY3LTAwMDAtYTFlYi03ZmExLTJjNz'\
#             'QzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlc'\
#             'mNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2Ft'\
#             'ZWFwaSIsImp0aSI6ImY1NDg0ZDAwLTFhMjItNG'\
#             'E2ZC1iNTQyLTRkYmI5Njk4NjhkMCIsImlhdCI6MTc'\
#             'yNDc4MzMxNSwic3ViIjoiZGV2ZWxvcGVyLzBhMDhjMjE'\
#             'xLTM1YmMtZWQ2NC02YTk4LTRiM2M2ZDE3NDJmZCIsInNjb3'\
#             'BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwMy4xNzkuOC4xNDUiXSwidHlwZSI6ImNsaWVudCJ9XX0.H0x22GLR32JCJI7pR3CByQTEN4LZsDNrgs2UrBDm-4ZGZFhi9Fcrigu3VwGYe5xt19sjhCJBnYnHbGE7ZZ-L9Q'
# import requests
#
# endpoint = 'https://api.clashofclans.com/v1/players/%G928VQGV9'
# res = requests.get(endpoint,{'authorization':})
# print(res.status_code)
# print(res.text)

# from utils import db_operations
#
# db_operations.create_user_wallet('adarsh')
# print(db_operations.get_user_balance_from_wallet('adarsh'))
# db_operations.update_user_wallet_balance('adarsh', 20)
# print(db_operations.get_user_balance_from_wallet('adarsh'))
# db_operations.update_user_wallet_balance('adarsh', 500)
# print(db_operations.get_user_balance_from_wallet('adarsh'))
# db_operations.update_user_wallet_balance('adarsh', 500)
# print(db_operations.get_user_balance_from_wallet('adarsh'))
# db_operations.update_user_wallet_balance('adarsh', 500)
# print(db_operations.get_user_balance_from_wallet('adarsh'))

# from transaction import Transaction
# from transaction_manager import TransactionManager
# t = Transaction(1000,'Adarsh','Sourabh','misc')
# print(t)
# print(TransactionManager.get_top_transactions())

# from datetime import datetime
# print(datetime.now())

# import re
# pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\w)(?!.* ).{8,}$'
# result = re.match(pattern,'adarsh13@')
# print(result.group())
#
# from utils import db_operations
# db_operations.create_user('adarsh1123','Adarsh@123')
# print(db_operations.check_if_user_exists('adarsh1123'))
#
# print(db_operations.check_all_users())

# import bcrypt
#
# # example password
# password = 'passwordabc'
#
# # converting password to array of bytes
# bytes = password.encode('utf-8')
#
# # generating the salt
# salt = bcrypt.gensalt()

# Hashing the password
# hash = bcrypt.hashpw(bytes, salt)
#
# # Taking user entered password
# userPassword = 'passwordabc'
#
# # encoding user password
# userBytes = userPassword.encode('utf-8')
# hash2 = bcrypt.hashpw(userBytes, salt)
# # checking password
# result = bcrypt.checkpw(hash2, hash)
#
# print(result)

# from utils import db_operations
# print(db_operations.get_last_n_transactions(10))

# li1 = [1, 2, 3]
# li2 = [4, 5, 6, 7]
# a = (set(li1).intersection(set(li2)))
# print(len(a))

# from authentication import Authentication
# import bcrypt
# user_pass = 'Ad123@'
# hashed_pass = Authentication.hash_password(user_pass)
#
# entered_pass = 'Ad123@'
# print(bcrypt.checkpw(entered_pass.encode('utf-8'),hashed_pass))

# from utils import db_operations
# print(db_operations.get_transaction(1))
# import re
# def check_username_format(username):
#
#     result = re.match(pattern, username)
#     if result.group():
#         return result.group() == username
#     else:
#         return False
#
# print(check_username_format('ad9306'))

# def transaction_printer(result):
#     for transaction in result:
#         amount, sender, receiver, category, transaction_id = tuple([transaction[i]
#                                                                     for i in range(len(transaction))])
#     transaction_repr = (f'--------------------------\n'
#                         f'Amount : {amount}\n'
#                         f'Sender : {sender}\n'
#                         f'Receiver : {receiver}\n'
#                         f'Category : {category}\n'
#                         f'Transaction_ID : {transaction_id}\n'
#                         f'------------------------------\n'
#                         )
#     print(transaction_repr, 'sdsd')
#
#
# transaction_printer([(1, 2, 3, 4, 5), (1, 2, 3, 4, 5)])
