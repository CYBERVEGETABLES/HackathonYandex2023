import sqlite3

conn = sqlite3.connect('data/HackathonYandex2023.sqlite')
cur = conn.cursor()


def user_is_registered(user_id: str) -> bool:
    sql_query = 'SELECT * FROM users WHERE id="{}"'
    res = cur.execute(sql_query.format(user_id))
    return res.rowcount != 0


def user_register(user_id: str, diary_login: str, diary_password: str) -> bool:
    sql_query = 'INSERT INTO users(id, diary_login, diary_password) VALUES("{}", "{}", "{}")'
    cur.execute(sql_query.format(user_id, diary_login, diary_password))
    return True


def user_get_diary_data(user_id: str) -> tuple[str, str]:
    sql_query = 'SELECT diary_login, diary_password FROM users WHERE id={}'
    res = cur.execute(sql_query.format(user_id)).fetchone()
    return res


def main():
    user_get_diary_data('1')


if __name__ == '__main__':
    main()
