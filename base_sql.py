import sqlite3

from config_data.config import CUR, CONNECT_BASE


def new_sql():

    # Создание таблиц
    CUR.execute("""CREATE TABLE IF NOT EXISTS 
        users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
         name TEXT,
          password TEXT,
           key TEXT,
           lesson INTEGER);
           """)
    CONNECT_BASE.commit()

    CUR.execute("""CREATE TABLE IF NOT EXISTS 
        lessons(
        lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        voice TEXT,
        video TEXT,
        discription TEXT);
           """)
    CONNECT_BASE.commit()

# Добавление данных в таблицу
# cur.execute("""INSERT INTO users(user_id, name, password, key)
#    VALUES('00001', 'Alex', 'Smith', 'male');""")
# connect_base.commit()

# cur.execute("SELECT lesson FROM users WHERE telegram_id='456';")
# print(cur.fetchone())
# three_results = cur.fetchall()
# print(three_results)

# DELETE FROM users WHERE lname='Parker'
# cursorObj.execute('UPDATE employees SET name = "Rogers" where id = 2')