import pytest
import allure
from utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/cats/{id}")
def test_delete_cat(api):
    logger.info("[API] Delete cat")

    # Arrange
    payload = build_cat_payload()
    with allure.step("Создаем кота"):
        logger.info(f"Создаем кота: {payload}")
        cat_id = api.create_cat(payload).json()["id"]

    # Act
    with allure.step(f"Удаляем по кота ID: {cat_id}"):
        logger.info(f"Удаляем по кота ID: {cat_id}")
        delete_resp = api.delete_cat(cat_id)

    with allure.step("Попытка получить кота по ID"):
        logger.info("Попытка получить кота по ID")
        get_deleted = api.get_cat_by_id(cat_id)

    # Assert
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем HTTP-статус получения"):
        logger.info(f"HTTP-статус удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"