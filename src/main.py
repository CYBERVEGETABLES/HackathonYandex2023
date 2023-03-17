import os

from dotenv import load_dotenv

from diary import DiaryNSO


def main():
    load_dotenv()

    diary = DiaryNSO(
        login=os.getenv('DIARY_LOGIN'),
        password=os.getenv('DIARY_PASSWORD'),
    )

    diary.auth()
    input()
    diary.quit()


if __name__ == '__main__':
    main()
