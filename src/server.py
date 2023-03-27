from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI()


@app.post('/')
async def main():
    return {
        'version': '1.0',
        'session': 'TODO',
        'response': {
            'text': 'Hello, World!',
            'end_session': 'false',
        },
    }


@app.get('/.well-known/acme-challenge/{key}')
async def acme_challenge(key: str):
    return FileResponse(f'.well-known/acme-challenge/{key}')
