import database
from yandex_functions import *


def build_response(text: str, session_id: str) -> dict:
    return {
        'version': '1.0',
        'session': session_id,
        'response': {
            'text': text,
            'end_session': 'false',
        },
    }


def handle(command: str, user_id: str) -> str:
    registered = database.user_is_registered(user_id)

    if not registered:
        register()

    if 'средний балл' in command:
        pass
