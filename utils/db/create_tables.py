from utils.db.connection import conn, cursor


def create_all_tables():
    create_table_user()
    create_table_transactions()
    create_table_wallets()


# def add_column():
#     cursor.execute("""alter table transactions add column minutes integer""")
#     conn.commit()

def create_table_transactions():
    cursor.execute(""" create table if not exists transactions 
    (
    id integer primary key,
    amount integer,
    receiver text,
    sender text,
    day integer,
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
                   '('
                   'username text not null,'
                   'password text not null,'
                   'email text not null,'
                   'mudra_pin integer not null'
                   ')'
                   )
    conn.commit()
