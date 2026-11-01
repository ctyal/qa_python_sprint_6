import pytest
import allure

from pages.main_page import MainPage
from data.data import MainPageFAQ

@allure.suite('Тестирование главной страницы сервиса Яндекс Самокат')
@allure.sub_suite('Оформление заказа самоката')
class TestMainPage:
    @allure.title('Проверка списка "Вопросы о Важном"')
    @allure.description('Проверка соотвествия ответов вопросам')
    @pytest.mark.parametrize("index", range(0, 8), ids=[
        "Вопрос 1 (Стоимость/Оплата)",
        "Вопрос 2 (Количество самокатов)",
        "Вопрос 3 (Время аренды)",
        "Вопрос 4 (Заказ на сегодня)",
        "Вопрос 5 (Продление/Возврат)",
        "Вопрос 6 (Зарядка)",
        "Вопрос 7 (Отмена заказа)",
        "Вопрос 8 (Доставка за МКАД)"
    ])
    def test_question_gets_the_right_answer_true(self, main_page, index):
        with allure.step('Открываем главную страницу Самоката'):
            main_page.open_main_page()
            
        with allure.step('Принимаем куки, если есть промпт'):
            main_page.accept_cookies()
            
        with allure.step('Скролл страницы к блоку вопросов'):
            main_page.scroll_to_faq()

        with allure.step (f'Клик по вопросу {index + 1}'):
            main_page.click_question(index)
              
        with allure.step(f'Проверка ответа на вопрос {index + 1}'):
            actual = main_page.get_answer_text(index)
            expected = expected = MainPageFAQ.answer_list[index]
            assert actual == expected, f"Ошибка в вопросе {index + 1}: ожидали '{expected}', получили '{actual}'"
