from threading import Thread
from typing import Callable, Any
from functools import wraps

import messages
from cache import DIARIES
from diary import DiaryNSO
from yandex_fuc import create_user_diary


def check_registred(func: Callable) -> Callable:
    print(1)
    @wraps(func)
    def work_model(user_id, *arg, **kargs) -> Any:
        if user_id not in DIARIES.keys():
            Thread(target=create_user_diary(user_id)).start()
            return messages.MESSAGE_DIARY_LOADING
        return func(user_id=user_id, user_diary=DIARIES[user_id], *arg, **kargs)
    work_model.__name__ = func.__name__
    return work_model


@check_registred
def next_day_schedule(user_diary: DiaryNSO, *arg, **kargs) -> str:
    print('get_next_day_schedule')
    if not user_diary.next_day_schedule:
        return messages.MESSAGE_READY_MODEL_ERROR
    return user_diary.get_next_day_schedule()


@check_registred
def next_day_homework(user_diary: DiaryNSO, *arg, **kargs) -> str:
    print('get_next_day_homework')
    if not user_diary.next_day_schedule:
        return messages.MESSAGE_READY_MODEL_ERROR
    return user_diary.get_next_day_homework()


@check_registred
def get_marks_per_quote(user_diary: DiaryNSO, text: str | None = None, *arg, **kargs) -> str:
    print('get_marks_per_quote')
    pass
