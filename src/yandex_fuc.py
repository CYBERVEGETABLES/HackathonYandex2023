import messages
import database
from cache import DIARIES
from diary import DiaryNSO


def create_user_diary(user_id) -> None:
    res = database.user_get_diary_data(user_id)
    diary_login, diary_password = res
    DIARIES[user_id] = DiaryNSO(diary_login, diary_password)


def register(user_id: str, diary_data: str) -> str:
    success = database.user_register(user_id, *diary_data.split())
    if success:
        return messages.MESSAGE_USER_WAS_REGISTERED

    return messages.MESSAGE_ERROR_OCCURRED
