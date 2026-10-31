from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from data.data import URL

class OrderPage(BasePage):
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

    def open_order_page(self):
        self.open_url(URL.url_order)

    def fill_personal_data(self, first_name, last_name, address, metro_station, phone):
        self.send_keys(self.first_name_input, first_name)
        self.send_keys(self.last_name_input, last_name)
        self.send_keys(self.address_input, address)

        self.click_element_js(self.metro_station_input)
        self.send_keys(self.metro_station_input, metro_station)
        target_station_locator = (By.XPATH, f"//ul[contains(@class, 'select-search')]//button[./div[text()='{metro_station}']]")
        self.wait_for_element_clickable(target_station_locator)
        self.click_element(target_station_locator)

        self.send_keys(self.phone_input, phone)

        self.wait_for_element_clickable(self.next_button)
        self.click_element_js(self.next_button)

    def fill_rent_data(self, date, rental_period, color, comment):
        self.wait_for_element_visible(self.date_input)
        self.click_element_js(self.date_input) 
        self.send_keys(self.date_input, date)
        self.press_enter(self.date_input)

        self.wait_for_element_clickable(self.rental_period_dropdown)
        self.click_element(self.rental_period_dropdown)
        rental_period_option = (By.XPATH, f"//div[@class='Dropdown-option' and text()='{rental_period}']")
        self.click_element(rental_period_option)
        if color:
            color_checkbox = (By.XPATH, f"//label[contains(text(), '{color}')]")
            self.click_element(color_checkbox)
        self.send_keys(self.comment_input, comment)
        self.click_element(self.order_button)

    def confirm_order(self):
        self.click_element(self.confirm_button)

    def check_confirmation_window_text(self):
        return self.wait_for_element_visible(self.confirmation_window_header).text
    