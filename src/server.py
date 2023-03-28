import json
from typing import Any

from fastapi import FastAPI
from fastapi import Request
# from fastapi.responses import FileResponse

import messages
import yandex


app = FastAPI()


@app.post('/')
async def main(request: Request) -> Any:
    request_data = json.loads(
        await request.body()
    )

    # if user is new
    if request_data['session']['new']:
        return yandex.build_response(
            text=messages.MESSAGE_START,
            session_id=request_data['session']['session_id']
        )

    response = yandex.handler(
        command=request_data['request']['original_utterance'],
        user_id=request_data['session']['user']['user_id']
    )

    return yandex.build_response(text=response, session_id=request_data['session']['session_id'])


# For Let's Encrypt
# @app.get('/.well-known/acme-challenge/{key}')
# async def acme_challenge(key: str):
#     return FileResponse(f'.well-known/acme-challenge/{key}')
