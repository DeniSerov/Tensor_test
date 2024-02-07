from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import sys
from icecream import ic
import os
import logging
import pytest
from logging.handlers import RotatingFileHandler


def init_rotating(filename, level=logging.INFO, prev_filename=None, log_name='log'):
    log_instance = logging.getLogger(log_name)
    log_instance.propagate = False
    if prev_filename is not None:
        for h in log_instance.handlers:
            h.flush()
            h.close()
            log_instance.removeHandler(h)
        os.rename(prev_filename, filename)
    log_instance.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(filename, maxBytes=100000, backupCount=2)
    log_instance.addHandler(handler)
    return log_instance

class BasePage():
    log = 'log/sbis'
    log_file = init_rotating(filename='%s.log' % (log))
    log_file_err = init_rotating(filename='%s.err' % (log), level=logging.ERROR, log_name="error")

    def __init__(self,driver):
        self.load_page = False
        self.driver = driver
        self.base_url = "https://sbis.ru"


    def clear_all_loggers(self):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    def print_and_log(self,message):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_message = str(date) + " " + str(self.base_url) + " " + str(message) + "\x0A"
        #print(data_message)
        self.log_file.info(msg=data_message)

    def print_report(self,message):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_message = str(date) + " " + str(self.base_url) + " " + str(message) + "\x0A"
        print(data_message)



    def log_mes_err(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        data_message = str(date) + " " + str(self.base_url) + " " + "Line_error = %s, type_error = %s" % (exc_traceback.tb_lineno, exc_value) + "\x0A"
        ic.disable()
        ic(data_message)
        self.log_file_err.error(data_message)

    def handle_error(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.log_mes_err()
        return wrapper

    def init_rotating(self, filename, level=logging.INFO, prev_filename=None, log_name='log'):
        log_instance = logging.getLogger(log_name)
        if prev_filename is not None:
            for h in log_instance.handlers:
                h.flush()
                h.close()
                log_instance.removeHandler(h)
            os.rename(prev_filename, filename)
        log_instance.setLevel(level)
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes=100000, backupCount=2)
        log_instance.addHandler(handler)
        return log_instance

    @handle_error
    def element_find(self,locator,timeout=10):
        self.print_and_log(f"Ищем и возвращаем элемент {locator}")
        return WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located(locator))

    @handle_error
    def check_title(self,title):
        self.print_and_log(f"Проверяем заголовок")
        if title in self.driver.title.lower():
            self.print_and_log(f"Заголовок корректен")
            return True
        else:
            self.print_and_log(f"Заголовок некорректен")
            return False

    @handle_error
    def check_url(self,url):
        self.print_and_log(f"Проверяем url")
        if url in self.driver.current_url:
            self.print_and_log(f"Url корректен")
            return True
        else:
            self.print_and_log(f"Url некорректен")
            return False


    @handle_error
    def scroll_to_element(self,locator,timeout=10):
        if self.element_find(locator,timeout):
            self.print_and_log(f"Пытаемся проктутить видимость до объекта {locator}")
            element = self.driver.find_element(locator[0],locator[1])
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)

    @handle_error
    def check_man(self,locator,timeout=10):
        self.print_and_log(f"Проверяем объект {locator}")
        if WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located(locator)):
            self.print_and_log(f"Найден объект {locator}")
            return True
        else:
            self.print_and_log(f"Не найден объект {locator}")
            return False

    @handle_error
    def click_hidden_button_tenzor(self,locator,timeout=10):
        self.print_and_log(f"Ищем и ожидаем объект {locator}")
        button = self.element_find(locator)
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        self.print_and_log(f"Пытаемся перевести курсор на {locator}")
        action = ActionChains(self.driver)
        action.move_to_element(button).click().perform()
        self.print_and_log(f"Успешное нажатие {locator}")

    @handle_error
    def switch_window(self,nom):
        self.print_and_log(f"Переключаемся на окно{nom}")
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[nom])

    @handle_error
    def driv_find(self,locator):
        self.print_and_log(f"Ищем объект из под драйвера {locator}")
        return self.driver.find_elements(locator[0],locator[1])

    @handle_error
    def start(self):
        self.print_and_log(f"Подключение к base_url {self.base_url}")
        try:
            self.load_page = False
            tmp = self.driver.get(self.base_url)
        except:
            self.chec_the_load()
        self.print_and_log("Подключение успешно")
        return tmp

    @handle_error
    def click_button(self,locator,timeout=10):
        self.print_and_log(f"Жмем на кнопку {locator}")
        button = self.element_find(locator,timeout)
        button.click()

    def chec_the_load(self):
        if not self.load_page:
            self.print_and_log("Подключение не удалось")
            pytest.fail(str("Точка входа не прогрузилась, завершаем тест"),False)
        else:
            self.load_page = True

