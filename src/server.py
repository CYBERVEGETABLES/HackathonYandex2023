import json

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse

import messages
import yandex


app = FastAPI()


@app.post('/')
async def main(request: Request):
    request_data = json.loads(
        await request.body()
    )

    # if user is new
    if request_data['session']['new']:
        return yandex.build_response(
            text=messages.MESSAGE_START,
            session_id=request_data['session']['session_id']
        )

    response = yandex.handle(
        command=request_data['request']['command'],
        user_id=request_data['session']['user']['user_id']
    )

    # TODO: REMOVE IN PROD
    print(f'{user_id=}')
    print(f'{user_new=}')
    print(f'{command=}')

    return yandex.build_response(text=response, session_id=request_data['session']['session_id'])


@app.get('/.well-known/acme-challenge/{key}')
async def acme_challenge(key: str):
    return FileResponse(f'.well-known/acme-challenge/{key}')
