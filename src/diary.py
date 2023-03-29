import os
import pickle
import time
from datetime import datetime
from threading import Thread
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from dotenv import load_dotenv


def get_tomorrow_date() -> str:
    """ Returns tomorrow date in format '%d.%m' """
    return f'{int(datetime.today().strftime("%d")) + 1}.{datetime.today().strftime("%m")}'


class DiaryNSO:
    def __init__(self, login: str, password: str):
        options = Options()
        options.add_argument('-headless')

        self.driver = webdriver.Firefox(options=options)

        self.login = login
        self.password = password
        
        Thread(target=self._update_controller).start()
            
    def _update_controller(self) -> NoReturn:
        while True:
            threads = []
            for func in (
                self.get_next_day_schedule,
                self.get_next_day_homework,
                self.get_final_grades_per_module,
                self.get_all_marks
            ):
                threads.append(Thread(target=func))
                threads[-1].start()
            for thread in threads:
                thread.join()
            time.sleep(60 * 30)

    def auth(self) -> bool:
        if os.path.exists(f'data/pkl/{self.login}.pkl'):
            with open(f'data/pkl/{self.login}.pkl', 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            print('INFO: Cookies loaded successfully')

        else:
            self.driver.get('https://school.nso.ru/authorize')

            form = self.driver.find_element(By.TAG_NAME, 'form')
            inputs = form.find_elements(By.TAG_NAME, 'input')

            counter = 0
            while self.driver.current_url != 'https://school.nso.ru/journal-app':
                inputs[0].send_keys(self.login)
                inputs[1].send_keys(self.password)
                form.find_element(By.TAG_NAME, 'button').click()

                time.sleep(1)

                counter += 1
                if counter == 5:
                    return False

            with open(f'data/pkl/{self.login}.pkl', 'wb') as file:
                pickle.dump(self.driver.get_cookies(), file)

            print('INFO: Cookies saved successfully')

        return True

    def get_next_day_schedule(self) -> None:
        self.next_day_schedule = None
        
        response = ''
        tomorrow_date = get_tomorrow_date()

        print(444)
        self.driver.get('https://school.nso.ru/journal-app')
        print(44)

        days = []
        while len(days) == 0:
            days = self.driver.find_elements(By.CLASS_NAME, 'dnevnik-day')
            time.sleep(2)

        for day in days:
            print(4)
            current_day_date = day.find_element(
                By.CLASS_NAME, 'dnevnik-day__title'
            ).text.split(', ')[1]

            if current_day_date == tomorrow_date:
                subjects = day.find_elements(By.CLASS_NAME, 'js-rt_licey-dnevnik-subject')

                if len(subjects) == 0:
                    return 'На завтра уроков не найдено'

                response = 'Завтра у Вас будут следующие предметы:\n' + \
                           '\n'.join([subject.text for subject in subjects])

        self.next_day_schedule = response

    def get_next_day_homework(self) -> None:
        self.next_day_homework = None
        
        response = ''
        tomorrow_date = get_tomorrow_date()

        if self.driver.current_url != 'https://school.nso.ru/journal-app':
            self.driver.get('https://school.nso.ru/journal-app')

        days = []
        while len(days) == 0:
            days = self.driver.find_elements(By.CLASS_NAME, 'dnevnik-day')
            time.sleep(2)

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

        self.next_day_homework = f'Домашнее задание на завтра:\n{response}'

    def get_final_grades_per_module(self) -> None:
        """ Это итоговые оценки по предметам за четверть без пустых хуёв
            короче, желаю удачи допилить дальше, я бессилен, пойду подрочу чтоль
            сделали в виде списка, чтобы легче дальше было делать"""
        # АХВХАХВАХ СЕРЕГА ТЫ ЕБЛАН Я ТЕБЯ ОБОЖАЮ
        # А я ему помог)))
        self.final_grades_per_module = None

        res = {}

        if self.driver.current_url != 'https://school.nso.ru/journal-student-grades-action':
            self.driver.get('https://school.nso.ru/journal-student-grades-action')

        subject = self.driver.find_elements(By.CLASS_NAME, 'cell')
        for i in subject:
            text = i.text.strip()
            if text is None:
                continue
            if '.' in text:
                try:
                    float(text)
                except TypeError:
                    continue
            else:
                continue
            res[i.get_attribute("name")] = float(text)
        self.final_grades_per_module = res

    def get_all_marks(self) -> None:
        self.all_marks = None
        
        res = []

        if self.driver.current_url != 'https://school.nso.ru/journal-student-grades-action':
            self.driver.get('https://school.nso.ru/journal-student-grades-action')

        subject = self.driver.find_elements(By.CLASS_NAME, 'cell')
        for i in subject:
            try:
                element = i.find_element(By.CLASS_NAME, 'cell-data')
            except NoSuchElementException:
                continue
            if element.text.strip() == '':
                continue

            source_mark = element.text.strip().split('✕')

            if '.' in source_mark[0]:
                continue
            mark = ('Н',)
            if '/' in source_mark[0]:
                mark = tuple(map(int, source_mark[0].split('/')))
            elif source_mark[0] != 'Н':
                if '-' in source_mark[0]:
                    mark = ((int(source_mark[0][:-1]), '-'),)
                else:
                    mark = (int(source_mark[0]),)
            res.append(
                {
                    'subject': i.get_attribute("name"),
                    'mark': mark,
                    'koef': int(source_mark[1]) if len(source_mark) == 2 else 1,
                    'date': i.get_attribute("mark_date").replace('-', '.')
                }
            )
        self.all_marks = res

    def quit(self):
        self.driver.quit()


def main():
    start = time.time()

    load_dotenv()

    diary = DiaryNSO(
        login=os.getenv('DIARY_LOGIN'),
        password=os.getenv('DIARY_PASSWORD'),
    )

    diary.auth()

    print(diary.get_next_day_schedule())
    # print(diary.get_next_day_homework())
    # print(diary.final_grades_per_module())
    # print(diary.get_all_marks())

    diary.quit()

    end = time.time() - start
    print(end)


if __name__ == '__main__':
    main()
