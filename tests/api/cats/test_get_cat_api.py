import pytest
import allure
from utils.data_builders import build_cat_payload, build_health_card, build_user_payload
from utils.models import assert_health_card, assert_cat_response, assert_adoption_data
from utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats/{id}")
def test_get_cat_with_health_card(api):
    logger.info("[API] get cat with health card")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    payload = build_health_card()
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, token)

    with allure.step("Обновление данных кота о новом владельце"):
        logger.info("Обновление данных кота о новом владельце")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Act
    with allure.step("Получаем созданного кота по Id"):
        logger.info("Получаем созданного кота по Id")
        get_resp = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Найденный кот: {get_resp}")
        allure.attach(str(get_resp), name="gotten cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp, cat_payload["name"], cat_payload["age"], cat_payload["breed"], cat_payload.get("history"), cat_payload.get("description"))
        assert_health_card(get_resp["healthCard"], payload["lastVaccination"], payload["medicalStatus"], payload.get("notes"))
        assert_adoption_data(get_resp, True, user_id)

