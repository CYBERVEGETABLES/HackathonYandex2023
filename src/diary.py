import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv


class DiaryNSO:
    def __init__(self, login: str, password: str):
        options = Options()
        # options.add_argument('-headless')
        self.driver = webdriver.Firefox(options=options)
        self.login = login
        self.password = password

    def auth(self):
        self.driver.get('https://school.nso.ru/authorize')

        form = self.driver.find_element(By.TAG_NAME, 'form')
        inputs = form.find_elements(By.TAG_NAME, 'input')

        while self.driver.current_url != 'https://school.nso.ru/journal-app':
            inputs[0].send_keys(self.login)
            inputs[1].send_keys(self.password)

            form.find_element(By.TAG_NAME, 'button').click()

            time.sleep(1)

    def get_next_day_schedule(self) -> str:
        def get_tomorrow_date() -> str:
            """ Returns tomorrow date in format '%d.%m' """
            return f'{int(datetime.today().strftime("%d")) + 1}.{datetime.today().strftime("%m")}'

        response = ''
        tomorrow_date = get_tomorrow_date()

        days = []
        while len(days) == 0:
            days = self.driver.find_elements(By.CLASS_NAME, 'dnevnik-day')

        for day in days:
            current_day_date = day.find_element(
                By.CLASS_NAME, 'dnevnik-day__title'
            ).text.split(', ')[1]

            if current_day_date == tomorrow_date:
                subjects = day.find_elements(By.CLASS_NAME, 'js-rt_licey-dnevnik-subject')

                if len(subjects) == 0:
                    return 'На завтра уроков не найдено'

                response = 'Завтра у Вас будут следующие предметы: ' + \
                           ', '.join([subject.text for subject in subjects])

        return response

    def get_next_day_homework(self) -> str:
        def get_tomorrow_date() -> str:
            """ Returns tomorrow date in format '%d.%m' """
            return f'{int(datetime.today().strftime("%d")) + 1}.{datetime.today().strftime("%m")}'

        response = ''
        tomorrow_date = get_tomorrow_date()

        days = []
        while len(days) == 0:
            days = self.driver.find_elements(By.CLASS_NAME, 'dnevnik-day')

        for day in days:
            current_day_date = day.find_element(
                By.CLASS_NAME, 'dnevnik-day__title'
            ).text.split(', ')[1]

            if current_day_date == tomorrow_date:
                lessons = day.find_elements(By.CLASS_NAME, 'dnevnik-lesson')

                for lesson in lessons:
                    try:
                        homework = lesson.find_element(By.CLASS_NAME, 'dnevnik-lesson__task')
                    except NoSuchElementException:
                        continue

                    subject = lesson.find_element(By.CLASS_NAME, 'js-rt_licey-dnevnik-subject').text
                    response += f'{subject}: {homework.text}\n'

        if response == '':
            return 'Домашнего задания на завтра не найдено'

        return f'Домашнее задание на завтра:\n{response}'

    def quit(self):
        self.driver.quit()


def main():
    load_dotenv()

    diary = DiaryNSO(
        login=os.getenv('DIARY_LOGIN'),
        password=os.getenv('DIARY_PASSWORD'),
    )

    diary.auth()
    print(diary.get_next_day_schedule())
    print(diary.get_next_day_homework())
    diary.quit()


if __name__ == '__main__':
    main()
