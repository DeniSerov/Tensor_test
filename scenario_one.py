import time
from BaseApp import BasePage
from selenium.webdriver.common.by import By
import requests
import os
import pytest

class sbisru_element:
    locator_contact_button = (By.CSS_SELECTOR, "li.sbisru-Header__menu-item:nth-child(2) > a:nth-child(1)")#li.sbisru-Header__menu-item:nth-child(2) > a:nth-child(1)
    locator_clientWidget = (By.CSS_SELECTOR, ".clientWidget-Button__icon")
    locator_tenzor_button = (By.CSS_SELECTOR, ".sbisru-Contacts__border-left--border-xm > a:nth-child(1) > img:nth-child(1)")
    locator_tenzor_power_in_men = (By.CSS_SELECTOR, ".tensor_ru-Index__block4-content")
    locator_tensor_video = (By.CSS_SELECTOR, ".tensor_ru-VideoBanner__video")
    locator_tensor_href_about = (By.CSS_SELECTOR, ".tensor_ru-Index__block4-content > p:nth-child(4) > a:nth-child(1)")
    locator_tensor_img_con = (By.XPATH,"//img[contains(@class, 'tensor_ru-About__block3')]")
    locator_region = (By.CSS_SELECTOR, ".ml-16 > span:nth-child(1)")
    locator_city = (By.CSS_SELECTOR, "#city-id-2")
    locator_parther = (By.XPATH,"//div[contains(@class, 'sbisru-Contacts-List__name')]")
    locator_camchatka = (By.CSS_SELECTOR, "li.sbis_ru-Region-Panel__item:nth-child(43) > span:nth-child(1)")
    locator_dow_sbis = (By.CSS_SELECTOR, "div.sbisru-Footer__cell:nth-child(10) > ul:nth-child(2) > li:nth-child(6) > a:nth-child(1)")
    locator_sbic_plagin = (By.XPATH, '''(//div[@class='controls-TabButton__caption' and contains(text(), 'СБИС Плагин')])''')
    locator_web_installer = (By.XPATH, '''(//div[contains(@class, 'sbis_ru-DownloadNew-loadLink')]/a[contains(text(), 'Скачать (Exe ')])''')
    locator_web_installer_visual = (By.CSS_SELECTOR,"#ws-c2ivo068to81707125754105 > div:nth-child(1) > p:nth-child(2)")
    locator_marker = (By.CLASS_NAME,"sbis_ru-DownloadNew-tabBanner")

class scenario(BasePage):
    def click_button_contact(self):
        self.print_report("Переходим в раздел контакты")
        self.element_find((sbisru_element.locator_clientWidget), 10)
        tmp = self.element_find((sbisru_element.locator_contact_button),10)
        tmp.click()

    def click_button_tenzor(self):
        self.print_report("Жмем на тензор")
        self.click_hidden_button_tenzor((sbisru_element.locator_tenzor_button), 40)

    def check_power_in_man(self):
        self.print_report("Проверяем что есть блок сила в людях")
        self.switch_window(1)
        self.check_man((sbisru_element.locator_tenzor_power_in_men))

    def click_about(self):
        self.print_report("Жмем на подробнее")
        time.sleep(2)
        self.scroll_to_element((sbisru_element.locator_tenzor_power_in_men), 10)
        self.click_hidden_button_tenzor((sbisru_element.locator_tensor_href_about), 10)
        self.check_title("https://tensor.ru/about")

    def compare_img(self):
        self.print_report("Сравниваем изображения")
        time.sleep(2)
        tmp = self.driv_find(sbisru_element.locator_tensor_img_con)
        if len(tmp) == 0:
            self.print_report("Изображений нет!")
            pytest.fail(str(""), False)
        img_width, img_height = tmp[0].get_attribute("width"),tmp[0].get_attribute("height")
        for img in tmp:
            if img.get_attribute("width") != img_width or img.get_attribute("height") != img_height:
                self.print_report("Изображения разного размера")
                pytest.fail(str(""), False)
        self.print_report("Изображения одинаковые")


    def compare_text(self,*args):
        time.sleep(1)
        self.print_report("Сравниваем текст")
        text_head = self.driv_find(sbisru_element.locator_region)
        text_city = self.driv_find(sbisru_element.locator_city)
        list_parther = self.driv_find(sbisru_element.locator_parther)
        if not args[0] in text_head[0].text or not args[1] in text_city[0].text or len(list_parther)<0:
            self.print_report(F"Текст не совпадает или нет партнеров. Нужен [{args[0]}] [{args[1]}], а получено [{text_head[0].text}] [{text_city[0].text}] [{len(list_parther)}]")
            pytest.fail(str(""), False)
            return False
        else:
            self.print_report("Текст совпадает, есть партнеры")

    def click_swipe_region(self):
        self.click_hidden_button_tenzor((sbisru_element.locator_region), 10)
        self.click_hidden_button_tenzor((sbisru_element.locator_camchatka), 10)

    def compare_title(self):
        self.print_report("Ищем нужный регион")
        self.check_title("Камчатский край")
        self.check_url("41-kamchatskij-kraj")
        self.print_report("Все совпало")

    def click_button_dowload_sbis(self):
        self.print_report("Щелкаем на скачать СБИС")
        self.element_find((sbisru_element.locator_clientWidget), 10)
        self.click_button((sbisru_element.locator_dow_sbis), 10)

    def find_dow(self):
        time.sleep(1)
        self.print_report("Вытаскиваем нужный элемент")
        self.element_find((sbisru_element.locator_marker), 10)
        self.click_hidden_button_tenzor((sbisru_element.locator_sbic_plagin), 10)


    def dowload_and_compare_file(self):
        element = self.element_find(sbisru_element.locator_web_installer)
        size_on_site = element.get_attribute("text")
        size_on_site = float(size_on_site[size_on_site.find("Exe ") + len("Exe "):size_on_site.rfind(" МБ")])
        name_file = element.get_attribute("href")
        self.print_report(f"Качаем файл {name_file}")
        r = requests.get(name_file)
        with open("tmp/%s" % (name_file[name_file.rfind("/") + 1:]), 'wb') as f:
            f.write(r.content)
        self.print_report(f"Успешно скачен {name_file}")
        file_size_bytes = os.path.getsize("tmp/%s" % (name_file[name_file.rfind("/") + 1:]))
        if round(file_size_bytes / (1024 * 1024), 2) == size_on_site:
            self.print_report(f"Размер файла совпадает")
        else:
            self.print_report("Файл не совпадает по размеру")
            pytest.fail(str(""), False)