import pytest
import allure
from utils.data_builders import build_cat_payload, build_health_card
from utils.models import assert_health_card
from utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats/{id}/health-card")
def test_create_health_card_success(api, auth_token):
    logger.info("[API] check health-card creation")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    payload = build_health_card()

    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
       assert_health_card(post_resp.json(), payload["lastVaccination"], payload["medicalStatus"], payload.get("notes"), cat_id)
