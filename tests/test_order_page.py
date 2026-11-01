import pytest
import allure

from data.data import URL, OrderData 
from pages.order_page import OrderPage
from pages.main_page import MainPage

@allure.suite('Тестирование страницы заказа Яндекс Самокат')
@allure.sub_suite('Оформление заказа самоката') 
class TestOrderFlow:
    @allure.title('Позитивный сценарий заказа самоката')
    @allure.description('Проверка создания заказа через разные точки входа')
    @pytest.mark.parametrize("click_button, user_data", [
        (MainPage.click_order_button_header, "set_1"),
        (MainPage.click_order_button_midpage, "set_2")
    ], ids=[
        "Заказ через кнопку в хедере: заполнены только обязательные поля",
        "Заказ через кнопку в центре страницы: заполнены все поля"    
    ])
    def test_order_scooter_successful(self, main_page, order_page, click_button, user_data):
        data = OrderData.data_set[user_data]

        with allure.step('Открываем главную страницу'):
            main_page.open_main_page()
        with allure.step('Принимаем куки, если есть промпт'):
            main_page.accept_cookies()
        with allure.step('Нажимаем кнопку "Заказать"'):
            click_button(main_page)
        with allure.step('Ожидаем загрузку страницы заказа'):
            main_page.wait_for_url_to_be(URL.url_order)
        with allure.step('Вносим валидные личные данные в форме "Для кого самокат" и кликаем "Далее"'):
            order_page.fill_personal_data(
                first_name=data["first_name"],
                last_name=data["last_name"],
                address=data["address"],
                metro_station=data["metro_station"],
                phone=data["phone"]
            )
        with allure.step('Вносим данные по аренде в форме "Про аренду" и кликаем "Заказать"'):
            order_page.fill_rent_data(
                date=data["date"],
                rental_period=data["rental_period"],
                color=data["color"],
                comment=data["comment"]
            )
        with allure.step('Подтверждаем заказ и проверяем успех'):
            order_page.confirm_order()
            actual_text = order_page.check_confirmation_window_text()
            assert "Заказ оформлен" in actual_text, f"Ожидалось 'Заказ оформлен', получено: '{actual_text}'"

@allure.suite('Тестирование страницы заказа Яндекс Самокат')
@allure.sub_suite('Редиректы логотипов в хедере') 
class TestLogoRedirections:
    @allure.title('Клик по логотипу "Самокат" возвращает на главную')
    def test_click_scooter_logo_directs_to_main_page_true(self, main_page, order_page):
        with allure.step('Открываем страницу заказа'):
            order_page.open_order_page()
        with allure.step('Кликаем по логотипу "Самокат" в хэдере'):
            order_page.click_scooter_logo()
        with allure.step('Проверяем, что осуществлён переход на главную страницу Яндекс Самокат'):
            assert main_page.wait_for_url_to_be(URL.url_main), f"Ожидался переход на {URL.url_main}. Текущий URL {main_page.get_current_url()}"

    @allure.title('Клик по логотипу "Яндекс" перенаправляет на "Дзен" в новом окне')
    def test_click_yandex_logo_directs_to_dzen_true(self, main_page, order_page):
        with allure.step('Открываем страницу заказа'):
            order_page.open_order_page()
        with allure.step('Кликаем по логотипу "Яндекс" в хэдере'):
            order_page.click_yandex_logo()
        with allure.step('Переходим на новую вкладку'):
            main_page.switch_to_new_window()
        with allure.step('Проверяем, что осуществлён переход на Яндекс Дзен'):
            assert main_page.wait_for_url_contains("dzen.ru"), (f"Переход на Дзен не осуществлен. Текущий URL: {main_page.get_current_url()}")
            