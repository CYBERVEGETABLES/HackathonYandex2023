import re

import database
import messages
from recognize import recognizer
from yandex_fuc import register


def build_response(text: str, session_id: str) -> dict:
    return {
        'version': '1.0',
        'session': session_id,
        'response': {
            'text': text,
            'end_session': 'false',
        },
    }


REGISTER_DATA_REGEXP = re.compile(r'^\w+\s+\w+$')


def handler(command: str, user_id: str) -> str | None:
    registered = database.user_is_registered(user_id)

    if not registered:
        return messages.MESSAGE_START

    if REGISTER_DATA_REGEXP.match(command):
        return register(user_id, command)

    answ = recognizer.get_answer(command)

    if isinstance(answ, tuple):
        return answ[-1](user_id)
    return answ
