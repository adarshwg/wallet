from user import User
from authentication import Authentication
from Errors import UserNotFoundError, InvalidPasswordError, WalletEmptyError

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
9. Exit
"""


def get_transaction_by_id(transaction_id,new_user):
    result = new_user.wallet.get_transaction_by_id(transaction_id,new_user.username)
    for transaction in result:
        transaction_id, amount, sender, receiver, month, year, category = tuple([transaction[i]
                                                                                 for i in range(len(transaction))])
        transaction_repr = (f'-------------Transaction------------- \n'
                            f'Amount : {amount}\n'
                            f'Sender : {sender}\n'
                            f'Receiver : {receiver}\n'
                            f'Month : {month}\n'
                            f'Year : {year}\n'
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


def wallet_functionalities(new_user):
    while True:
        wallet_input = input(wallet_message)
        if wallet_input == '1':
            print('User balance is :', new_user.get_user_balance())
        elif wallet_input == '2':
            new_transaction = get_new_transaction_values()
            try :
                new_user.update_amount(
                    new_transaction['amount'],
                    new_transaction['sender'],
                    new_transaction['receiver'],
                    new_transaction['category']
                )
                print('Transaction has been added successfully !')
            except WalletEmptyError:
                print('User wallet is empty :(')

        elif wallet_input == '3':
            transaction_id = int(input('Enter the transaction id : '))
            get_transaction_by_id(transaction_id,new_user)
        elif wallet_input == '4':
            number = input('Enter the number of transactions (default :10) :')
            if not number:
                number = 10
            list_of_transactions = new_user.wallet.get_last_n_transactions(new_user.username,number)
            for transaction in list_of_transactions:
                get_transaction_by_id(transaction[0],new_user)

        elif wallet_input == '5':
            number = input('Enter the number of transactions (default :10) :')
            if not number:
                number = 10
            list_of_top_transactions = new_user.wallet.get_top_n_transactions(new_user.username,number)
            for transaction in list_of_top_transactions:
                get_transaction_by_id(transaction[0],new_user)

        elif wallet_input == '6':
            current_month_transactions = new_user.wallet.get_current_month_transactions(new_user.username)
            for transaction in current_month_transactions:
                get_transaction_by_id(transaction[0],new_user)
        elif wallet_input == '7':
            month = int(input('Enter the month in number : '))
            year = input('Enter the year : ')
            selected_month_transactions = new_user.wallet.get_transactions_by_month(month, year, new_user.username)
            for transaction in selected_month_transactions:
                get_transaction_by_id(transaction[0],new_user)

        elif wallet_input == '8':
            print(new_user.wallet)
        elif wallet_input == '9' :
            return
        else:
            print('Please enter valid input from the options !')
            continue
        call_again = input('Do you wish to continue ?\n y/n : ')
        if call_again.lower() == 'y':
            wallet_functionalities(new_user)
        else:
            return


def login_function():
    username = input('Enter your username : ')
    password = input('Enter your password : ')
    username_check = Authentication.check_username_format(username)
    password_check = Authentication.check_password_format(password)
    if not username_check or not password_check:
        print('Enter valid username and password format!!')
        return
    try:
        if User.login(username,password):
            Authentication.check_if_username_exists(username)
            user_object = User(username,password)
            wallet_functionalities(user_object)
    except UserNotFoundError :
        print('User was not found!')

    except InvalidPasswordError:
        print('Invalid password entered !!\n')
        continued = input('Do you wish to try again?\n y/n : ')
        if continued.lower() == 'n':
            return
        else:
            login_function()


def caller_function() :
    user_input = input(auth_message)
    if user_input == '1':
        login_function()
    elif user_input == '2':
        username = input('Enter your username :')
        password = input('Enter your password :')
        new_user = User(username, password)
        wallet_functionalities(new_user)
    elif user_input == '3' :
        return 0

while True:
    call_end = caller_function()
    if call_end :
        break
    continued = input('Do you wish to continue ?\n y/n : ')
    if continued.lower() == 'y':
        call_end = caller_function()
        if call_end :
            break
    else:
        break
