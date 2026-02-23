import pytest
import allure
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_users_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USERS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения всех пользователей без регистрации"):
        logger.info("Попытка получения всех пользователей без регистрации")
        get_resp = api.get_all_users()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_user_by_Id_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USER BY ID][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения пользователя по Id без регистрации"):
        logger.info("Попытка получения пользователя по Id без регистрации")
        get_resp = api.get_user_by_id(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_adopted_cats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения котов пользователя без регистрации"):
        logger.info("Попытка получения котов пользователя без регистрации")
        get_resp = api.get_adopted_cats_by_userId(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)