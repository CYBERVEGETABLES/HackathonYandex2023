import sqlite3

conn = sqlite3.connect('data/HackathonYandex2023.sqlite')
cur = conn.cursor()


def user_is_registered(user_id: str) -> bool:
    sql_query = 'SELECT * FROM users WHERE id="{}"'
    res = cur.execute(sql_query.format(user_id))
    return res.rowcount != 0


def user_register(user_id: str, diary_login: str, diary_password: str) -> None:
    sql_query = 'INSERT INTO users(id, diary_login, diary_password) VALUES("{}", "{}", "{}")'
    cur.execute(sql_query.format(user_id, diary_login, diary_password))
