import pytest
import allure
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_patch_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка обновления данных кота"):
        logger.info("Попытка обновления данных кота")
        patch_resp = api.patch_cat(1, {"name": "TestCat_UpdatedName"})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_adopt_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[ADOPT CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка обновления данных кота о новом владельце"):
        logger.info("Попытка обновления кота о новом владельце")
        patch_resp = api.adopt_cat(1, {"userId": 1})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)