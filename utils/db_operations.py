import sqlite3
from Errors import UserNotFoundError, InvalidPasswordError,WalletEmptyError
from datetime import datetime

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()


def create_table_transactions():
    cursor.execute(""" create table if not exists transactions 
    (
    id integer primary key,
    amount integer,
    receiver text,
    sender text,
    month integer,
    year integer,
    category text
    )
    """)
    conn.commit()


def create_table_wallets():
    cursor.execute('create table if not exists wallets  '
                   '(username text not null,'
                   'amount integer)'
                   )
    conn.commit()


def create_table_user():
    cursor.execute('create table if not exists user  '
                   '(username text not null,'
                   'password text not null)'
                   )
    conn.commit()


create_table_user()
create_table_transactions()
create_table_wallets()


def check_if_user_exists(username):
    cursor.execute('select * from user where username=?', (username,))
    conn.commit()
    return cursor.fetchall() != []


def create_user(username, password):
    if check_if_user_exists(username):
        return
    cursor.execute('insert into user values (?,?)', (username, password))
    conn.commit()


def get_hashed_user_password(username):
    cursor.execute('select password from user where username=?', (username,))
    conn.commit()
    hashed_password_list = cursor.fetchall()
    if hashed_password_list:
        return hashed_password_list[0][0]
    else:
        raise UserNotFoundError


def create_user_wallet(username: str):
    create_table_wallets()
    cursor.execute('insert into wallets values (?,0)', (username,))
    conn.commit()


def get_user_balance_from_wallet(username: str):
    cursor.execute('select amount from wallets where username=?', (username,))
    res = cursor.fetchall()
    if res:
        return res[0][0]
    else:
        raise UserNotFoundError('User not found!')


def check_if_user_wallet_exists(username: str):
    cursor.execute('select amount from wallets where username=?', (username,))
    res = cursor.fetchall()
    if res:
        return True
    else:
        return False


def update_user_wallet_balance(username: str, amount: int):
    current_amount = get_user_balance_from_wallet(username)
    if amount < 0 and current_amount + amount < 0:
        raise WalletEmptyError('User wallet is empty!!')
    cursor.execute('update wallets set amount= ? where username= ?', (current_amount + amount, username))
    conn.commit()


def insert(amount: int, receiver: str, sender: str, year: int, month: int, category: str = 'misc') -> None:
    cursor.execute('insert into transactions values (null,?,?,?,?,?,?)',
                   (amount, receiver, sender, month, year, category))
    conn.commit()


def get_transaction(transaction_id,username):
    cursor.execute('select * from transactions where id= ? and (sender=? or receiver=?)', (transaction_id,username,username))
    transaction = cursor.fetchall()
    return transaction


def get_current_transaction_id():
    res = cursor.execute('select max(id) from transactions')
    return res.fetchall()[0][0]


def get_top_n_transactions(username,requested_transactions=10):
    cursor.execute('select * from transactions where (sender=? or receiver=?) order by amount desc limit ?', (username,username,requested_transactions,))
    res = cursor.fetchall()
    return res


def get_last_n_transactions(username,requested_transactions=10):
    cursor.execute('select * from transactions where (sender=? or receiver=?) order by id desc limit ?', (username,username,requested_transactions))
    res = cursor.fetchall()
    return res


def get_transaction_by_month(month, year,username):
    cursor.execute('select * from transactions where month=? and year=? and (sender=? or receiver = ?)', (month, year,username,username))
    res = cursor.fetchall()
    return res


def get_current_month_transactions(username):
    current_datetime = datetime.now().date()
    return get_transaction_by_month(current_datetime.month, current_datetime.year,username)
