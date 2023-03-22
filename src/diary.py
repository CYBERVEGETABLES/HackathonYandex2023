import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv


class DiaryNSO:
    def __init__(self, login: str, password: str):
        options = Options()
        # options.add_argument('-headless')
        # self.driver = webdriver.Firefox(options=options)
        self.driver = webdriver.Chrome(options=options)
        self.login = login
        self.password = password

    def auth(self):
        self.driver.get('https://school.nso.ru/authorize')

        form = self.driver.find_element(By.TAG_NAME, 'form')

        inputs = form.find_elements(By.TAG_NAME, 'input')
        inputs[0].send_keys(self.login)
        inputs[1].send_keys(self.password)

        form.find_element(By.TAG_NAME, 'button').click()

    def get_today_marks(self) -> str:
        what = 'расписание на неделю'  # пользователь говорит что хочет, либо оценки, либо расписание :)
        response = list()
        time.sleep(2)
        # TODO реализовать кнопку, чтобы переключала недели
        self.driver.get('https://school.nso.ru/journal-app/u.931/week.1')
        days = self.driver.find_elements(By.CLASS_NAME, 'dnevnik-day')
        if 'оцен' in what and what.isalnum():
            for i in days:
                if '13.03' in i.text:  # здесь также рандомное число, но позже будет дата
                    massiv = (i.text).split('\n')
            for j in range(len(massiv)):
                if len(massiv[j]) == 1 and massiv[j].isdigit():
                    stroka = massiv[j - 1] + " " + massiv[j]
                    response.append(stroka)
            if len(response) != 0:
                for i in response:
                    print(i)
            else:
                print("В этот день у вас нет оценок")
        elif 'расп' in what and 'недел' in what:
            massiv = list()
            for k in days:
                massiv.append(k.text.split('\n'))
            for t in range(len(massiv)):
                response.append(massiv[t][0])
                for w in range(len(massiv[t])):
                    if len(massiv[t][w]) == 2 and massiv[t][w][1] == '.':
                        if ':' in massiv[t][w + 1] and ('0' in massiv[t][w + 1] or '1' in massiv[t][w + 1]):
                            stroka = massiv[t][w] + " " + massiv[t][w + 2]
                        else:
                            stroka = massiv[t][w] + " " + massiv[t][w + 1]
                        response.append(stroka)
            if len(response) != 0:
                for i in response:
                    print(i)
            else:
                print("У вас нет уроков!")

    def quit(self):
        self.driver.quit()
#так ...

def main():
    load_dotenv()

    diary = DiaryNSO(
        login=os.getenv('DIARY_LOGIN'),
        password=os.getenv('DIARY_PASSWORD'),
    )

    diary.auth()
    print(diary.get_today_marks())
    input()
    diary.quit()


if __name__ == '__main__':
    main()
