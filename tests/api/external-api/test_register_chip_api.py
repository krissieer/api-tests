import pytest
import allure
from utils.models import assert_chip_registration
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cexternal-api/roskot/register-chip")
def test_register_chip_success(api, roskot_api_key):
    logger.info("[API] register chip in roskot")

    # Arrange 
    payload = {"name": "Test_Cat", "breed": "Test_Cat"}
    
    # Act
    with allure.step("Регистрируем кота"):
        logger.info(f"Регистрируем кота: {payload}")
        resp = api.register_chip(payload, api_key=roskot_api_key)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус регистрации: {resp.status_code}")
        assert resp.status_code == 201, f"Ожидалось 201, получено {resp.status_code}"

    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_chip_registration(resp.json())


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cexternal-api/roskot/register-chip Boundary name's values")
@pytest.mark.parametrize("invalid_name", ["", "A", " "], ids=["empty name", "one_char name", "space"])
def testregister_chip_invalid_name(api, invalid_name, roskot_api_key):
    logger.info("[API] borderline name length")
    
    # Arrange
    payload = {f"name": invalid_name, "breed": "Test_Cat"}

    # Act
    with allure.step(f"Регистрируем кота с именем: '{invalid_name}' "):
        logger.info(f"Регистрируем кота с именем: '{invalid_name}'")
        resp = api.register_chip(payload, api_key=roskot_api_key)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    
    
@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cexternal-api/roskot/register-chip Boundary breed's values")
@pytest.mark.parametrize("invalid_breed", ["", "A", " "], ids=["empty", "one_char", "space"])
def test_register_chip_invalid_breed(api, invalid_breed, roskot_api_key):
    logger.info("[API] borderline brees length")
    
    # Arrange
    payload = {f"name": "Test_Cat", "breed": invalid_breed}

    # Act
    with allure.step(f"Регистрируем кота с породой: '{invalid_breed}' "):
        logger.info(f"Регистрируем кота с породой: '{invalid_breed}'")
        resp = api.register_chip(payload, api_key=roskot_api_key)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cexternal-api/roskot/register-chip Invalid api-key")
def test_register_chip_invalid_api_key(api):
    logger.info("[API] wrong api-key")

    # Arrange
    payload = {"name": "Test_Cat", "breed": "Test_Cat"}

    # Act
    with allure.step("Регистрируем кота с неверным api-key"):
        logger.info("Регистрируем кота с неверным api-key")
        resp = api.register_chip(payload, api_key="wrong_api_key")

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cexternal-api/roskot/register-chip empty api-key")
def test_register_chip_empty_api_key(api):
    logger.info("[API] api-key is not provided")

    # Arrange
    payload = {"name": "Test_Cat", "breed": "Test_Cat"}

    # Act
    with allure.step("Регистрируем кота без api-key"):
        logger.info("Регистрируем кота без api-key")
        resp = api.register_chip(payload, api_key="")

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"