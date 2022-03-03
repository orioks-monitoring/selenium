from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import json
import pickle
from utils.yandex_disk import YandexDisk
from dataclasses import dataclass
import config


def my_isdigit(x) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False


def login_via_logpass(browser):
    url = 'https://orioks.miet.ru/user/login'
    browser.get(url)
    time.sleep(4)
    if url != browser.current_url:
        return print('[Browser] Страница недоступна')

    csrf_value = browser.find_element(By.CSS_SELECTOR, 'input[name="_csrf"]').get_attribute('value')

    username = browser.find_element(By.ID, 'loginform-login')
    password = browser.find_element(By.ID, 'loginform-password')

    username.send_keys(config.ORIOKS_LOGPASS['login'])
    password.send_keys(config.ORIOKS_LOGPASS['password'])

    rememberme = browser.find_element(By.ID, 'loginform-rememberme')
    if rememberme.get_attribute('value') == 0:
        rememberme.click()
    browser.find_element(By.ID, 'loginbut').click()
    time.sleep(5)

    pickle.dump(browser.get_cookies(), open('cookies.pkl', 'wb'))
    url = 'https://orioks.miet.ru/student/student'
    browser.get(url)


def login_via_cookies(browser):
    url = 'https://orioks.miet.ru/student/student'
    browser.get(url)
    cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get(url)


@dataclass
class DisciplineBall:
    current: float = 0
    might_be: float = 0


def get_forang(browser) -> dict:
    """return: [{'subject': s, 'tasks': [t], 'ball': {'current': c, 'might_be': m}, ...]"""
    forang_raw = browser.find_element(By.ID, 'forang').get_attribute('innerHTML')

    forang = json.loads(forang_raw)

    json_to_save = []
    for discipline in forang['dises']:
        discipline_ball = DisciplineBall()
        one_discipline = []
        for mark in discipline['segments'][0]['allKms']:
            alias = mark['sh']
            
            current_grade = mark['grade']['b']
            max_grade = mark['max_ball']

            one_discipline.append({'alias': alias, 'current_grade': current_grade, 'max_grade': max_grade})
            discipline_ball.current += current_grade if my_isdigit(current_grade) else 0
            discipline_ball.might_be += max_grade if my_isdigit(max_grade) and current_grade != '-' else 0
        json_to_save.append({
            'subject': discipline['name'],
            'tasks': one_discipline,
            'ball': {
                'current': discipline_ball.current,
                'might_be': discipline_ball.might_be,
            }
        })
    student_id = forang['student']['numst']
    return (student_id, json_to_save)


async def get_student_info():
    browser = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.FIREFOX)
    browser.implicitly_wait(10)

    await YandexDisk.download(filename='cookies.pkl')
    try:
        login_via_cookies(browser)
    except:
        login_via_logpass(browser)
        await YandexDisk.upload(filename='cookies.pkl')

    student_id, detailed_info = get_forang(browser)
    browser.quit()
    os.remove('cookies.pkl')

    return (student_id, detailed_info)
