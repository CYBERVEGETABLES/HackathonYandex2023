import sqlite3

conn = sqlite3.connect('data/HackathonYandex2023.sqlite')
cur = conn.cursor()

__all__ = (
    'user_is_registered',
    'user_register',
    'user_get_diary_data',
    'init',
    'conn',
    'cur'
)


def user_is_registered(user_id: str) -> bool:
    sql_query = 'SELECT id FROM users WHERE id="{}"'
    res = cur.execute(sql_query.format(user_id)).fetchone()
    return len(res) == 1


def user_register(user_id: str, diary_login: str, diary_password: str) -> bool:
    sql_query = 'INSERT INTO users(id, diary_login, diary_password) VALUES("{}", "{}", "{}")'
    cur.execute(sql_query.format(user_id, diary_login, diary_password))
    conn.commit()
    return True


def user_get_diary_data(user_id: str) -> tuple[str, str] | None:
    sql_query = 'SELECT diary_login, diary_password FROM users WHERE id="{}"'
    res = cur.execute(sql_query.format(user_id)).fetchone()
    return res


def init() -> None:
    conn.execute(
        'CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, diary_login TEXT, diary_password TEXT)'
    )
    conn.commit()
