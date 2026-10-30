from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from data.data import *

class MainPage:
    cookie_accept_button = (By.XPATH, "//button[text()='Да все привыкли']")
    cookie_container = (By.XPATH, "//*[contains(@class, 'App_CookieConsent')]")
    order_button_header = (By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[text()='Заказать']")
    order_button_midpage = ((By.XPATH, "//div[contains(@class, 'Home_ThirdPart')]//button[text()='Заказать']"))

    scooter_logo = (By.XPATH, "//*[contains(@class, 'Header_LogoScooter')]")
    yandex_logo = (By.XPATH, "//*[contains(@class, 'Header_LogoYandex')]")

    faq = (By.CLASS_NAME, "accordion")
    # получение локатора вопроса (0-7)
    @staticmethod
    def get_question(index):
        return (By.ID, f"accordion__heading-{index}")
    # получение локатора ответа (0-7); ответы в data.py
    @staticmethod
    def get_answer(index):
        return (By.ID, f"accordion__panel-{index}")
    
    def __init__(self, driver):
        self.driver = driver

    def open_main_page(self):
        self.driver.get(URL.url_main)

    def accept_cookies(self):
        try:
            cookie_button = WebDriverWait(self.driver, 2).until(ec.element_to_be_clickable(self.cookie_accept_button))
            self.driver.execute_script("arguments[0].click();", cookie_button) 
            WebDriverWait(self.driver, 5).until(ec.invisibility_of_element_located(self.cookie_container))
        except:
            pass

    def scroll_to_faq(self):
        faq_element = self.driver.find_element(*self.faq)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", faq_element)    

    def click_order_button_header(self):
        self.driver.find_element(*self.order_button_header).click()

    def click_order_button_midpage(self):
        button = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located(self.order_button_midpage))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()

    def click_question(self, index):
        question = WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(self.get_question(index)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question)
        WebDriverWait(self.driver, 2).until(ec.element_to_be_clickable(self.get_question(index)))
        question.click()
        
        WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(self.get_answer(index)))
        
    def get_answer_text(self, index):
        answer = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(self.get_answer(index)))
        return answer.text

    def get_expected_answer(self, index):
        return MainPageFAQ.answer_list[index]

    def check_answer_matches(self, index):
        self.click_question(index)

        actual = self.get_answer_text(index)
        expected = self.get_expected_answer(index)

        return actual, expected

    def click_scooter_logo(self):
        self.driver.find_element(*self.scooter_logo).click()

    def click_yandex_logo(self):
        self.driver.find_element(*self.yandex_logo).click()

    def wait_for_url_to_be(self, expected_url, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.url_to_be(expected_url))
            return True
        except:
            return False
        
    def switch_to_new_window(self, timeout=5):
        WebDriverWait(self.driver, timeout).until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def wait_for_url_contains(self, text, timeout=20):
            try:
                WebDriverWait(self.driver, timeout).until(ec.url_contains(text))
                return True
            except:
                return False

    def get_current_url(self):
        return self.driver.current_url
