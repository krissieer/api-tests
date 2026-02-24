import pytest
import allure
from utils.data_builders import build_user_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint with token")
def test_get_users_authorized_contract(api, openapi_validator, auth_token):
    logger.info("[GET USERS][POSITIVE] authorized")
    
    # Act
    with allure.step("Получениe всех пользователей"):
        logger.info("Получениe всех пользователей")
        get_resp = api.get_all_users(token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)

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
@allure.story("Protected endpoint with token")
def test_get_user_by_Id_authorized_contract(api, openapi_validator):
    logger.info("[GET USER BY ID][POSITIVE] authorized")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    # Act
    with allure.step("Получаем user_id из списка всех пользователей"):
        logger.info("Получаем user_id из списка всех пользователей")
        users = api.get_all_users(token=token)
        user_id = next(u["id"] for u in users.json() if u["login"] == user_payload["login"])

    # Act
    with allure.step("Получениe пользователя по Id"):
        logger.info("Получениe пользователя по Id")
        get_resp = api.get_user_by_id(user_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
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
@allure.story("Protected endpoint with token")
def test_get_adopted_cats_authorized_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][POSITIVE] authorized")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    with allure.step("Получаем user_id из списка всех пользователей"):
        logger.info("Получаем user_id из списка всех пользователей")
        users = api.get_all_users(token=token)
        user_id = next(u["id"] for u in users.json() if u["login"] == user_payload["login"])

    # Act
    with allure.step("Получениe котов пользователя"):
        logger.info("Получениe котов пользователя")
        get_resp = api.get_adopted_cats_by_userId(user_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
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