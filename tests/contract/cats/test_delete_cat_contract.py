import pytest
import allure
from utils.data_builders import build_cat_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint with token")
def test_delete_cat_authorized_contract(api, openapi_validator, auth_token):
    logger.info("[DELETE CAT][POSITIVE] authorized")
    
    # Arrange
    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]
    
    # Act
    with allure.step("Удаление кота по Id"):
        logger.info("Удаление кота по Id")
        resp = api.delete_cat(cat_id, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 204, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_delete_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[DELETE CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка удаления кота без регистрации"):
        logger.info("Попытка удаления кота  без регистрации")
        resp = api.delete_cat(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)