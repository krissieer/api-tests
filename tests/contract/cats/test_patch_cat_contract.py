import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint with token")
def test_patch_cat_authorized_contract(api, openapi_validator, auth_token):
    logger.info("[PATCH CAT][POSITIVE] authorized")
    
    # Arrange
    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Обновление данных кота"):
        logger.info("Обновление данных кота")
        patch_resp = api.patch_cat(cat_id, {"name": "TestCat_UpdatedName"}, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


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
@allure.story("Protected endpoint with token")
def test_adopt_cat_authorized_contract(api, openapi_validator):
    logger.info("[ADOPT CAT][POSITIVE] authorized")
    
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

    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Обновление данных кота о новом владельце"):
        logger.info("Обновление кота о новом владельце")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
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