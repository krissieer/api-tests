import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload, generate_unique_login
import logging
logger = logging.getLogger(__name__)


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("User Registration")
def test_register_new_user_success(api, auth_token):
    logger.info("[Integration] Successful new user registration")

    # Arrange
    user_data = generate_unique_login()

    # Act
    with allure.step("Регистрация"):
        resp = api.register(user_data)
        allure.attach(str(user_data), name="User login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Получаем всех пользователей"):
        users = api.get_all_users(token=auth_token).json()
        allure.attach(str(users), name="Cat after", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем наличие зарегистрированного пользователя в списке"):
        assert any(u["login"] == user_data["login"] for u in users)
        

@pytest.mark.integration
@allure.feature("Integration")
def test_invalid_registration(api, auth_token):
    logger.info("[Integration] Checking the immutability of the DB when trying to redister invalid user")
    
    # Arrange
    payload = {"firstName": 'firstName', "lastName": "lastName", "login": "", "password": "short"}

    # Act
    with allure.step("Получаем исходный список пользователей"):
        initial_resp = api.get_all_users(token=auth_token).json()
        allure.attach(str(initial_resp), name="Users", attachment_type=allure.attachment_type.JSON)  
    
    with allure.step("Регистрация с невалидными данными"):
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="Invalid payload", attachment_type=allure.attachment_type.JSON)          

    with allure.step("Получаем список после попытки добавленияя"):
        after_resp = api.get_all_users(token=auth_token).json()
        allure.attach(str(after_resp), name="users after failed registration", attachment_type=allure.attachment_type.JSON)  

    # Assert
    with allure.step("Сравниваем количество до и после попытки регистрации"):
        initial_count = len(initial_resp)
        after_count = len(after_resp)
        assert after_count == initial_count, f"Ожидалось {initial_count}, получено {after_count}"

