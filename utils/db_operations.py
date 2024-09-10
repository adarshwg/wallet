from utils.connection import conn, cursor
from Errors import UserNotFoundException, InvalidPasswordException, WalletEmptyException


def check_if_user_exists(username):
    cursor.execute('select * from user where username=?', (username,))
    conn.commit()
    return cursor.fetchall() != []

def delete_user():
    cursor.execute('drop table user')

def create_user(username, password):
    if check_if_user_exists(username):
        return
    cursor.execute('insert into user values (?,?)', (username, password))
    conn.commit()


def get_hashed_user_password(username):
    if not check_if_user_exists(username):
        raise UserNotFoundException
    cursor.execute('select password from user where username=?', (username,))
    conn.commit()
    hashed_password_list = cursor.fetchall()
    return hashed_password_list[0][0]


def create_user_wallet(username: str):
    cursor.execute('insert into wallets values (?,0)', (username,))
    conn.commit()


def get_user_balance_from_wallet(username: str):
    cursor.execute('select amount from wallets where username=?', (username,))
    res = cursor.fetchall()
    if res:
        return res[0][0]
    else:
        raise UserNotFoundException('User not found!')


def check_if_user_wallet_exists(username: str):
    cursor.execute('select * from wallets where username=?', (username,))
    res = cursor.fetchall()
    if res:
        return True
    else:
        return False


def update_user_wallet_balance(username: str, amount: int):
    current_amount = get_user_balance_from_wallet(username)
    if amount < 0 and current_amount + amount < 0:
        raise WalletEmptyException('Not enough balance in the wallet!!')
    cursor.execute('update wallets set amount= ? where username= ?', (current_amount + amount, username))
    conn.commit()


def insert(amount: int, receiver: str, sender: str, month: int, year: int, category: str = 'misc') -> None:
    if not category:
        category = 'misc'
    cursor.execute('insert into transactions values (null,?,?,?,?,?,?)',
                   (amount, receiver, sender, month, year, category))
    conn.commit()


def get_transaction(transaction_id, username):
    cursor.execute('select * from transactions where id= ? and (sender=? or receiver=?)',
                   (transaction_id, username, username))
    transaction = cursor.fetchall()
    return transaction


def get_current_transaction_id():
    cursor.execute('select max(id) from transactions')
    return cursor.fetchall()[0][0]


def get_top_n_transactions(username, requested_transactions=10):
    # if not isinstance(requested_transactions,int):
    #     requested_transactions = 10
    cursor.execute('select * from transactions where (sender=? or receiver=?) order by amount desc limit ?',
                   (username, username, requested_transactions,))
    res = cursor.fetchall()
    return res


def get_last_n_transactions(username, requested_transactions=10):
    # if not isinstance(requested_transactions,int):
    #     requested_transactions = 10
    cursor.execute('select * from transactions where (sender=? or receiver=?) order by id desc limit ?',
                   (username, username, requested_transactions))
    res = cursor.fetchall()
    return res


def get_transaction_by_month(month, year, username):
    cursor.execute('select * from transactions where month=? and year=? and (sender=? or receiver = ?)',
                   (month, year, username, username))
    res = cursor.fetchall()
    return res
