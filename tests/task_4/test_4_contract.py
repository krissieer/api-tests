import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload, generate_unique_login
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.task4
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register success")
def test_register_contract_success(api, openapi_validator):
    logger.info("[REGISTER][POSITIVE] valid payload")
    
    # Arrange
    payload = generate_unique_login()

    # Act
    with allure.step("Регистрируемся"):
        resp = api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 201, f"Ожидалось 201, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.task4
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register duplicate login")
def test_register_contract_duplicate(api, openapi_validator):
    logger.info("[REGISTER][NEGATIVE] duplicate login")

    # Arrange
    payload = generate_unique_login()

    # Act
    with allure.step("Регистрируемся"):
        api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Регистрируемся повторно с тем же логином"):
        reg_second_resp = api.register(payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert reg_second_resp.status_code == 409, f"Ожидалось 409, получено {reg_second_resp.status_code}"
    
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(reg_second_resp)


BOUNDARY_PAYLOADS = [
    ({"firstName": "  ", "lastName": "  "}, "spaces"),
    ({"firstName": "A", "lastName": "A"}, "too short 'firstName' and 'lastName'"),
    ({"firstName": "", "lastName": ""}, "empty fields")]
@pytest.mark.task4
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register Boundary: user's name length")
@pytest.mark.parametrize("payload, description", BOUNDARY_PAYLOADS)
def test_create_cat_namesboundary_contract(api, openapi_validator, payload, description):
    logger.info("[REGISTER][NEGATIVE] borderline name length")
    
    # Arrange
    payload = {
        "firstName": payload['firstName'],
        "lastName": payload['lastName'],
        "login": "TestLogin",
        "password": "TestPassword"
    }
    
    # Act
    with allure.step(f"Попытка зарегистрироваться с данными: {description}"):
        resp = api.register(payload)
        allure.attach(str(payload), name="Invalid user's name", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено { resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)



BOUNDARY_PAYLOADS = [
    ({"login": "", "password": ""}, "empty fields"),
    ({"login": "  ", "password": "  "}, "spaces"),
    ({"login": "TestLogin", "password": "1"}, "1 symbol password"),
    ({"login": "TestLogin", "password": "12345"}, "5 symbol password")]
@pytest.mark.task4
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register Boundary: login data length")
@pytest.mark.parametrize("payload, description", BOUNDARY_PAYLOADS)
def test_create_cat_namesboundary_contract(api, openapi_validator, payload, description):
    logger.info("[REGISTER][NEGATIVE] borderline login data length")
    
    # Arrange
    payload = {
        "firstName": "TestUser_firstName",
        "lastName": "TestUser_lastName",
        "login": payload['login'],
        "password": payload['password']
    }
    
    # Act
    with allure.step(f"Попытка зарегистрироваться с данными: {description}"):
        resp = api.register(payload)
        allure.attach(str(payload), name="Invalid login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)





