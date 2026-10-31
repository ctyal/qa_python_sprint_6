from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class BasePage:
    scooter_logo = (By.XPATH, "//*[contains(@class, 'Header_LogoScooter')]")
    yandex_logo = (By.XPATH, "//*[contains(@class, 'Header_LogoYandex')]")
    cookie_accept_button = (By.XPATH, "//button[text()='да все привыкли']")
    cookie_container = (By.XPATH, "//*[contains(@class, 'App_CookieConsent')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10) # Общий таймаут 10 сек

    def open_url(self, url):
        self.driver.get(url)

    def accept_cookies(self):
        try:
            self.click_element_js(self.cookie_accept_button)
            self.wait.until(ec.invisibility_of_element_located(self.cookie_container))
        except:
            pass

    def wait_for_element_visible(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator):
        return self.wait.until(ec.element_to_be_clickable(locator))

    def click_element(self, locator):
        element = self.wait_for_element_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def click_element_js(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.send_keys(text)

    def find_element(self, locator):
        return self.wait.until(ec.presence_of_element_located(locator))

    def wait_for_url_to_be(self, expected_url, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.url_to_be(expected_url))
            return True
        except:
            return False

    def wait_for_url_contains(self, text, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(ec.url_contains(text))
            return True
        except:
            return False
        
    def switch_to_new_window(self, timeout=5):
        WebDriverWait(self.driver, timeout).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_current_url(self):
        return self.driver.current_url

    def press_enter(self, locator):
        self.find_element(locator).send_keys(Keys.ENTER)

    def click_scooter_logo(self):
        self.click_element(self.scooter_logo)

    def click_yandex_logo(self):
        self.click_element(self.yandex_logo)      
