from user import User
from authentication import Authentication

auth_message = """
Choose an option :
1. Login to account
2. Sign up as user\n
"""

wallet_message = """
Choose an option :
1. See wallet amount 
2. Add a transaction
3. Get transaction by id
4. Get last n transactions 
5. Get top n transactions
6. Get current month transactions
7. Get transactions by month 
8. See wallet
"""


def get_transaction_by_id():
    transaction_id = int(input('Enter the transaction id : '))
    result = new_user.wallet.get_transaction_by_id(transaction_id)
    for transaction in result:
        amount, sender, receiver, category, transaction_id = tuple([transaction[i]
                                                                    for i in range(5)])

    transaction_repr = (f'--------------------------\n'
                        f'Amount : {amount}\n'
                        f'Sender : {sender}\n'
                        f'Receiver : {receiver}\n'
                        f'Category : {category}\n'
                        f'Transaction_ID : {transaction_id}\n'
                        f'------------------------------\n'
                        )
    print(transaction_repr)


def get_new_transaction_values():
    amount = int(input('Enter the amount involved : '))
    sender = input('Enter the sender : ')
    receiver = input('Enter the receiver : ')
    category = input('Enter the category : ')
    return {
        'amount': amount,
        'sender': sender,
        'receiver': receiver,
        'category': category
    }


def wallet_functionalities():
    while True:
        wallet_input = input(wallet_message)
        if wallet_input == '1':
            print('User balance is :', new_user.get_user_balance())
        elif wallet_input == '2':
            new_transaction = get_new_transaction_values()
            new_user.update_amount(
                new_transaction['amount'],
                new_transaction['sender'],
                new_transaction['receiver'],
                new_transaction['category']
            )
            print('Transaction has been added successfully !')
        elif wallet_input == '3':
            get_transaction_by_id()
        elif wallet_input == '4':
            number = input('Enter the number of transactions (default :10) :')
            if not number :
                number = 10
            print(new_user.wallet.get_last_n_transactions(number))
        elif wallet_input == '5':
            number = input('Enter the number of transactions (default :10) :')
            if not number :
                number = 10
            print(new_user.wallet.get_top_n_transactions(number))

        elif wallet_input == '6':
            print(new_user.wallet.get_current_month_transactions())
        elif wallet_input == '7':
            month = int(input('Enter the month in number : '))
            year = input('Enter the year : ')
            print(new_user.wallet.get_transactions_by_month(month, year))
        elif wallet_input == '8':
            print(new_user.wallet)
        else:
            continue
        call_again = input('Do you wish to continue ?\n y/n : ')
        if call_again.lower() == 'y':
            wallet_functionalities()
        else:
            return


while True:
    user_input = input(auth_message)
    if user_input == '1':
        username = input('Enter your username : ')
        password = input('Enter your password : ')
        username_check = Authentication.check_username_format(username)
        password_check = Authentication.check_password_format(password)
        if not username_check or not password_check:
            print('Enter valid username and password !!')
        new_user = User(username, password)
        if new_user.login:
            wallet_functionalities()

        else:
            print('Invalid password entered !!\n')
            continued = input('Do you wish to try again?\n y/n : ')
            if continued.lower() == 'n':
                break
    elif user_input == '2':
        username = input('Enter your username :')
        password = input('Enter your password :')
        new_user = User(username, password)

    continued = input('Do you wish to continue ?\n y/n : ')
    if continued.lower() == 'y':
        wallet_functionalities()
    else:
        break
