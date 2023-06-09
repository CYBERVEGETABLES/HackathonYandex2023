import re

from recognize import recognizer
from yandex_fuc import register


def build_response(text: str, session_id: str) -> dict:
    return {
        'version': '1.0',
        'session': session_id,
        'response': {
            'text': str(text),
            'end_session': 'false',
        },
    }


REGISTER_DATA_REGEXP = re.compile(r'^\w+\s+\w+$')


def handler(command: str, user_id: str) -> str | None:
    if REGISTER_DATA_REGEXP.match(command):
        return register(user_id, command)

    answer = recognizer.get_answer(command)
    print(answer)

    if isinstance(answer, tuple):
        res =  answer[-1](user_id, text=answer[0])
        print(res)
        return res

    return answer
