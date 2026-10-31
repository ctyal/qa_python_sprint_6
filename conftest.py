import pytest
from selenium import webdriver

from pages.main_page import MainPage
from pages.order_page import OrderPage

@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def order_page(driver):
    return OrderPage(driver)