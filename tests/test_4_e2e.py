import pytest
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response, generate_unique_login
import logging
logger = logging.getLogger(__name__)


@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Registration and adoption")
def test_registration_and_adoption_flow(api):
    logger.info("[End-to-End][POSITIVE] Registration and adoption")

    # Arrange 
    login_payload = {"login": "test_user", "password": "password123"}
    # Act
    with allure.step("Попытка авторизоваться без регистрации"):
        login_resp = api.login(login_payload)
        allure.attach(str(login_payload), name="Login data", attachment_type=allure.attachment_type.JSON)
    # Assert 
    with allure.step("Проверяем, что авторизация не прошла"):
        assert login_resp.status_code == 401, f"Ожидалось 401, получено {login_resp.status_code}"

    # Arrange 
    register_payload = generate_unique_login()
    # Act
    with allure.step("Регистрация"):
        register_resp = api.register(register_payload)
        allure.attach(str(register_payload), name="Register data", attachment_type=allure.attachment_type.JSON)
    # Assert 
    with allure.step("Проверяем успешную регистрацию"):
        assert register_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
        assert "access_token" in register_resp.json()

    # Arrange 
    token = register_resp.json()["access_token"]
    cat_payload = {"name": generate_unique_cat_name(),"age": 1,"breed": "Bengal"}
    # Act
    with allure.step("Создание кота"):
        cat_resp = api.create_cat(cat_payload, token=token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = cat_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert cat_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
    
    # Act 
    with allure.step("Получаем всех пользователей"):
        users = api.get_all_users(token=token)
        allure.attach(str(users.json()), name="User", attachment_type=allure.attachment_type.JSON)
    # Assert 
    with allure.step("Проверяем получение списка пользователей"):
        assert users.status_code == 200, f"Ожидалось 200, получено {create_resp.status_code}"
        assert len(users.json()) > 0, f"Ожидалось, что количество пользователей > 0, получено {len(users.json())}"
    
    # Arrange 
    user_id = users.json()[0]["id"]
    # Act 
    with allure.step("Обновляем данные кота о владельце"):
        adopt_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)
    # Assert 
    with allure.step("Проверяем усыновление"):    
        assert adopt_resp.status_code == 200, f"Ожидалось 200, получено {adopt_resp.status_code}"
    with allure.step("Проверяем данные кота"):    
        cat = api.get_cat_by_id(cat_id).json()
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)
        assert cat["isAdopted"] is True, f"Ожидалось True, получено {cat['isAdopted']}"
        assert cat["owner"]["id"] == user_id, f"Ожидалось {user_id}, получено {cat['owner']['id']}"
    with allure.step("Получаем данные пользователя с кошками"):
        user = api.get_adopted_cats_by_userId(user_id, token).json()
        allure.attach(str(user), name="Gotten user", attachment_type=allure.attachment_type.JSON)
        assert len(user["cats"]) == 1, f"Ожидалось 1, получено {len(user['cats'])}"
        assert user["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user['cats'][0]['id']}"
