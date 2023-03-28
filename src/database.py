import sqlite3

base = sqlite3.connect('data/HackathonYandex2023.sqlite')
cur = base.cursor()

__all__ = (
    'user_is_registered',
    'user_register',
    'user_get_diary_data',
    'init_db',
    'base',
    'cur'
)

def user_is_registered(user_id: str) -> bool:
    sql_query = 'SELECT * FROM users WHERE id="{}"'
    res = cur.execute(sql_query.format(user_id))
    return res.rowcount != 0


def user_register(user_id: str, diary_login: str, diary_password: str) -> bool:
    sql_query = 'INSERT INTO users(id, diary_login, diary_password) VALUES("{}", "{}", "{}")'
    cur.execute(sql_query.format(user_id, diary_login, diary_password))
    return True


def user_get_diary_data(user_id: str) -> tuple[str, str] | None:
    sql_query = 'SELECT diary_login, diary_password FROM users WHERE id={}'
    res = cur.execute(sql_query.format(user_id)).fetchone()
    return res

def init_db() -> None:
    base.execute(
        'CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, diary_login text, diary_password text) '
    )
    base.commit()


def main():
    user_get_diary_data('1')


if __name__ == '__main__':
    main()
