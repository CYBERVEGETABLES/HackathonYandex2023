from threading import Thread

import messages
from cache import DIARIES
from yandex_fuc import create_user_diary


def next_day_schedule(user_id: str) -> str:
    if user_id in DIARIES.keys():
        return DIARIES[user_id].get_next_day_schedule()

    Thread(target=create_user_diary(user_id)).start()
    return messages.MESSAGE_DIARY_LOADING


def next_day_homework(user_id: str) -> str:
    if user_id in DIARIES.keys():
        return DIARIES[user_id].get_next_day_homework()

    Thread(target=create_user_diary(user_id)).start()
    return messages.MESSAGE_DIARY_LOADING
