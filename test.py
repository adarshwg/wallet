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

from datetime import datetime
print(datetime.now())