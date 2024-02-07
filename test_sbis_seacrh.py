from scenario_one import scenario
import logging
from logging.handlers import RotatingFileHandler
import os
import logging


class Test_sbisru_headClass():
    "Выполнение сценариев на сбис"
    def test_sbisru_one(self,browser):
        "Первый сценарий"
        dc = scenario(browser)
        dc.start()
        dc.click_button_contact()
        dc.click_button_tenzor()
        dc.check_power_in_man()
        dc.click_about()
        dc.compare_img()
        dc.clear_all_loggers()

    def test_sbisru_two(self,browser):
        "Второй сценарий"
        dc = scenario(browser)
        dc.start()
        dc.click_button_contact()
        dc.compare_text("Нижегородская обл.","Нижний Новгород")
        dc.click_swipe_region()
        dc.compare_text("Камчатский край","Петропавловск-Камчатский")
        dc.compare_title()
        dc.clear_all_loggers()

    def test_sbisru_three(self,browser):
        "Третий сценарий"
        dc = scenario(browser)
        dc.start()
        dc.click_button_dowload_sbis()
        dc.find_dow()
        dc.dowload_and_compare_file()
        dc.clear_all_loggers()