import pytest
import allure
from utils.data_builders import build_cat_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_create_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[CREATE CAT][NEGATIVE] Unauthorized")
    
    # Arrange
    cat_payload = build_cat_payload()
    
    # Act
    with allure.step(f"Попытка создания кота"):
        logger.info(f"Попытка создания кота: {cat_payload}")
        resp = api.create_cat(cat_payload)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)