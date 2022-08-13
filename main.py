from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from model_param import *


def selenium_scrapper():
    # Если нет катоалога для хранения страниц сайта, то создаем его
    curr_dir = os.getcwd()
    dir_path = f'{curr_dir}\\{SITE_DATA_FOLDER}'
    # Если в катологе есть какие либо файлы с расширением html, удаляем их
    if not os.path.isdir(dir_path):
        os.mkdir(SITE_DATA_FOLDER)
    for f in os.listdir(dir_path):
        if not f.endswith(".html"):
            continue
        os.remove(os.path.join(dir_path, f))
    count = 1

    while count <= MAX_AMNT_SITE_PAGE:
        # Формируем адрес страницы:
        if count > 1:
            url = f'{URL_FORM}?g={URL_PARAMETERS["g"]}&page={count}&spm={URL_PARAMETERS["spm"]}'
            # url = f'{URL_FORM}?g={URL_PARAMETERS["g"]}&page={count}'
        else:
            url = f'{URL_FORM}?g={URL_PARAMETERS["g"]}&spm={URL_PARAMETERS["spm"]}'
            # url = f'{URL_FORM}?g={URL_PARAMETERS["g"]}'
        # Загружаем страницу
        driver.get(url)
        # Прокручиваем до конца страницу
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        sleep(PAUSE_DURATION_SECONDS)
        # Вытаскиваем содержимое...
        page_source = driver.page_source
        if SAFE_IN_FILE_KEY:
            # сохраняем в файл
            file_name = f'{dir_path}\\page_source_{count}.html'
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(page_source)
        sleep(PAUSE_DURATION_SECONDS)
        # Проверяем страницу на пустоту:
        if page_source.find("SearchWrap_SearchError__wordsWrap__oy8dw") > -1:
            break
        count += 1
    print('Selenium_skrapper отработал.')
    print('Количество вытащенных и сохраненных страниц: {0}. '.format(count))


def main():
    selenium_scrapper()


if __name__ == '__main__':
    try:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        main()
    except Exception as e:
        print(e)
    finally:
        driver.quit()
