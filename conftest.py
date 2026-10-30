import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()
    