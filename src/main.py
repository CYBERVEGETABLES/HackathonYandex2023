import os
import uvicorn


def main():
    uvicorn.run(
        'server:app',
        host='0.0.0.0',
        port=443,
        workers=os.cpu_count(),
        reload=True,

        ssl_keyfile='./.ssl/privkey.pem',
        ssl_certfile='./.ssl/fullchain.pem',
    )


if __name__ == '__main__':
    main()
