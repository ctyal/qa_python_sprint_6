from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from data.data import *

class OrderPage:
    first_name_input = (By.XPATH, "//input[@placeholder='* Имя']")
    last_name_input = (By.XPATH, "//input[@placeholder='* Фамилия']")
    address_input = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    metro_station_input = (By.XPATH, "//input[@placeholder='* Станция метро']")
    phone_input = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    next_button = (By.XPATH, "//button[text()='Далее']")

    date_input = (By.XPATH, "//input[contains(@placeholder, 'Когда привезти самокат')]")
    rental_period_dropdown = (By.CLASS_NAME, "Dropdown-control")
    comment_input = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    order_button = (By.XPATH, "//div[contains(@class, 'Order_Buttons')]/button[text()='Заказать']")

    confirm_button = (By.XPATH, "//button[contains(@class, 'Button_Middle') and contains(text(), 'Да')]")
    confirmation_window_header = (By.XPATH, "//*[contains(@class, 'Order_ModalHeader')]")

    def __init__(self,driver):
        self.driver = driver

    def fill_personal_data(self, first_name, last_name, address, metro_station, phone):
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.address_input).send_keys(address)

        metro_input = self.driver.find_element(*self.metro_station_input)
        self.driver.execute_script("arguments[0].click();", metro_input)
        metro_input.send_keys(metro_station)
        target_station_locator = (By.XPATH, f".//ul//button[./div[text()='{metro_station}']]")
        suggested_station = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(target_station_locator))
        suggested_station.click()

        self.driver.find_element(*self.phone_input).send_keys(phone)
        next_btn = self.driver.find_element(*self.next_button)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.next_button)).click()

    def fill_rent_data(self, date, rental_period, color, comment):
        set_date = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(self.date_input))
        self.driver.execute_script("arguments[0].click();", set_date)
        set_date.send_keys(date)
        set_date.send_keys(Keys.ENTER)
        dropdown = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.rental_period_dropdown))
        dropdown.click()
        rental_period_option = (By.XPATH, f"//div[@class='Dropdown-option' and text()='{rental_period}']")
        self.driver.find_element(*rental_period_option).click()
        if color:
            color_checkbox = (By.XPATH, f"//label[contains(text(), '{color}')]")
            self.driver.find_element(*color_checkbox).click()
        self.driver.find_element(*self.comment_input).send_keys(comment)
        self.driver.find_element(*self.order_button).click()

    def confirm_order(self):
         WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable(self.confirm_button)).click()

    def check_confirmation_window_text(self):
        confirmation = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(self.confirmation_window_header))
        return confirmation.text
    