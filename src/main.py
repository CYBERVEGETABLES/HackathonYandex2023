import os
import uvicorn


def main():
    uvicorn.run(
        'server:app',
        host='0.0.0.0',
        port=8080,
        workers=os.cpu_count(),

        # TODO: выпустить сертификат с помощью Let's encrypt и настроить HTTPS
        # ssl_keyfile='./localhost+4-key.pem',
        # ssl_certfile='./localhost+4.pem',
    )


if __name__ == '__main__':
    main()
