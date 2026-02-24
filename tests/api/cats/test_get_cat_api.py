import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
from utils.models import assert_cat_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats/{id}")
def test_get_cat_by_id(api):
    logger.info("[API] Get cat by Id")

    # Arrange 
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    payload = build_cat_payload()
    
    with allure.step("Создаём кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload, token=token)
        cat_id = create_resp.json()["id"]
        allure.attach(str(payload), name="created cat", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем созданного кота по Id без токена"):
        logger.info("Получаем созданного кота по Id без токена")
        get_resp_no_auth = api.get_cat_by_id(cat_id)
        logger.debug(f"Найденный кот: {get_resp_no_auth.json()}")
        allure.attach(str(get_resp_no_auth.json()), name="gotten cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статусы"):
        logger.info(f"HTTP-статус получения без токена: {get_resp_no_auth.status_code}")
        assert get_resp_no_auth.status_code == 200, f"Ожидалось 200, получено {get_resp_no_auth.status_code}"

    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp_no_auth.json(), payload["name"], payload["age"], payload["breed"], payload.get("history"), payload.get("description"))