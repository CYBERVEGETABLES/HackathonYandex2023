from threading import Thread

import database
import messages
from cache import DIARIES
from diary import DiaryNSO


def register(user_id: str, diary_data: str) -> str:
    success = database.user_register(user_id, *diary_data.split())
    if success:
        return messages.MESSAGE_USER_WAS_REGISTERED

    return messages.MESSAGE_ERROR_OCCURRED


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


def create_user_diary(user_id) -> None:
    diary_login, diary_password = database.user_get_diary_data(user_id)
    DIARIES[user_id] = DiaryNSO(diary_login, diary_password)
