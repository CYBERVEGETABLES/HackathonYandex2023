import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

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
        inputs[0].send_keys(self.login)
        inputs[1].send_keys(self.password)

        form.find_element(By.TAG_NAME, 'button').click()

    def quit(self):
        self.driver.quit()


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
