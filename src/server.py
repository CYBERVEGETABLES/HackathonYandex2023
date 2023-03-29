import json
from typing import Any

from fastapi import FastAPI
from fastapi import Request
# from fastapi.responses import FileResponse

import messages
import yandex
import database


app = FastAPI()


@app.post('/')
async def main(request: Request) -> Any:
    request_data = json.loads(
        await request.body()
    )

    user_id = request_data['session']['user']['user_id']
    user_registered = database.user_is_registered(user_id)

    # if chat just started
    if request_data['session']['new']:
        if user_registered:
            text = messages.MESSAGE_START_USER_REGISTERED
        else:
            text = messages.MESSAGE_START_USER_NOT_REGISTERED

        return yandex.build_response(
            text=text,
            session_id=request_data['session']['session_id']
        )

    response = yandex.handler(
        command=request_data['request']['original_utterance'],
        user_id=user_id
    )

    return yandex.build_response(text=response, session_id=request_data['session']['session_id'])


# For Let's Encrypt
# @app.get('/.well-known/acme-challenge/{key}')
# async def acme_challenge(key: str):
#     return FileResponse(f'.well-known/acme-challenge/{key}')
