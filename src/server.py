from fastapi import FastAPI

app = FastAPI()


@app.post('/')
def main():
    return {
        'version': '1.0',
        'session': 'TODO',
        'response': {
            'text': 'Hello, World!',
            'end_session': 'false',
        },
    }
