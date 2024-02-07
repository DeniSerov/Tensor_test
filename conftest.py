import pytest
from selenium import webdriver
import allure


@pytest.fixture(scope="session")
def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()


def pytest_collection_modifyitems(items):
    test_name= {"test_sbisru_one": "Первый сценарий",#
         "test_sbisru_two": "Второй сценарий",#
         "test_sbisru_three": "Третий сценарий",}
    for item in items:
        a_temp = str(item._nodeid)
        if "test_sbisru" in str(item) and test_name.get(a_temp[a_temp.rfind(":")+1:]):
            item._nodeid = a_temp[a_temp.rfind(":")+1:].replace(a_temp[a_temp.rfind(":")+1:],test_name.get(a_temp[a_temp.rfind(":")+1:]))