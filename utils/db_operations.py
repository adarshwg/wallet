import sqlite3
from wallet_empty import sad_song_player
from datetime import datetime
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

cursor.execute(""" create table if not exists transactions 
(
id integer primary key,
amount integer,
receiver text,
sender text,
category text,
year integer,
month integer
)
""")


class UserNotFoundError(Exception):
    pass


class WalletEmptyError(Exception):
    pass


def create_table_wallets():
    cursor.execute('create table if not exists wallets  '
                   '(username text not null,'
                   'amount integer)'
                   )
    conn.commit()


def create_user_wallet(username: str):
    print('here to create user wallet! -----')
    create_table_wallets()
    cursor.execute('insert into wallets values (?,0)', (username,))
    print(f'inserted into the db {username}')
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
        sad_song_player.player()
        raise WalletEmptyError('User wallet is empty!!')
    cursor.execute('update wallets set amount= ? where username= ?', (current_amount + amount, username))
    print('updated the user amount in the wallet', current_amount + amount, username)
    conn.commit()


def insert(amount: int, sender: str, receiver: str, year: int, month: int, category: str = 'misc') -> None:
    cursor.execute('insert into transactions values (null,?,?,?,?,?,?)',
                   (amount, sender, receiver, year, month, category))
    print('inserted the data!!!!')
    conn.commit()


def get_transaction(transaction_id):
    cursor.execute(f'select * from transactions where id={transaction_id}')
    return cursor.fetchall()


def get_current_transaction_id():
    res = cursor.execute('select max(id) from transactions')
    return res.fetchall()[0][0]


def get_top_n_transactions(requested_transactions):
    cursor.execute('select * from transactions order by amount desc limit ?', (requested_transactions,))
    res = cursor.fetchall()
    return res


def get_last_n_transactions(requested_transactions):
    cursor.execute('select * from transactions order by id desc limit ?', (requested_transactions,))
    res = cursor.fetchall()
    return res


def get_current_month_transactions() :
    cursor.execute('select * from transactions where month=?', (datetime.now().date().month,))
    res = cursor.fetchall()
    return res
