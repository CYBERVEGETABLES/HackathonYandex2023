import re

import database
import yandex_functions
import messages


def build_response(text: str, session_id: str) -> dict:
    return {
        'version': '1.0',
        'session': session_id,
        'response': {
            'text': text,
            'end_session': 'false',
        },
    }


REGISTER_DATA_REGEXP = re.compile(r'^\w\s\w$')


def handle(command: str, user_id: str) -> str:
    registered = database.user_is_registered(user_id)

    if not registered:
        return messages.MESSAGE_START

    if 'домашн' in command:
        return yandex_functions.next_day_homework(user_id)

    elif 'расписание' in command:
        return yandex_functions.next_day_schedule(user_id)

    elif REGISTER_DATA_REGEXP.match(command):
        return yandex_functions.register(user_id, command)

    else:
        return messages.MESSAGE_UNKNOWN_COMMAND
