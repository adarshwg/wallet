import sqlite3

conn = sqlite3.connect('number.db')
cursor = conn.cursor()

cursor.execute("""
    create table if not exists number(
    id integer primary key
    )
""")
conn.commit()


def get_number():
    result = cursor.execute('select * from number').fetchall()
    return result


def insert_number():
    cursor.execute('insert into number values (null)', ())


def update_number():
    cursor.execute('update id from number ')
