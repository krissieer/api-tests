import pytest
import allure
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_delete_user_unauthorized_contract(api, openapi_validator):
    logger.info("[DELETE USER][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка удаления пользователя без регистрации"):
        logger.info("Попытка удаления пользователя без регистрации")
        delete_resp = api.delete_user(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 401, f"Ожидалось 401, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)