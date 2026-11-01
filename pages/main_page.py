import allure
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from pages.base_page import BasePage 
from data.data import URL

class MainPage(BasePage):
    order_button_header = (By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[text()='Заказать']")
    order_button_midpage = ((By.XPATH, "//div[contains(@class, 'Home_ThirdPart')]//button[text()='Заказать']"))

    faq = (By.CLASS_NAME, "accordion")
    # получение локатора вопроса (0-7)
    @staticmethod
    def get_question(index):
        return (By.ID, f"accordion__heading-{index}")
    # получение локатора ответа (0-7); ответы в data.py
    @staticmethod
    def get_answer(index):
        return (By.ID, f"accordion__panel-{index}")

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        self.open_url(URL.url_main)

    @allure.step("Скроллить к FAQ")
    def scroll_to_faq(self):
        faq_element = self.find_element(self.faq)
        self.scroll_to_element(faq_element)

    @allure.step("Кликнуть на кнопку 'Заказать' в хедере")
    def click_order_button_header(self):
        self.click_element(self.order_button_header)

    @allure.step("Кликнуть на кнопку 'Заказать' на середине страницы")
    def click_order_button_midpage(self):
        self.click_element(self.order_button_midpage)

    @allure.step("Открыть вопрос с индексом {index}")    
    def click_question(self, index):
        self.click_element_js(self.get_question(index))
        self.wait_for_element_visible(self.get_answer(index))

    @allure.step("Получить текст ответа с индексом {index}")    
    def get_answer_text(self, index):
        return self.wait_for_element_visible(self.get_answer(index)).text
