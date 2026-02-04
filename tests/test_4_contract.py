import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload, generate_unique_login
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

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


INVALID_PAYLOADS = [
    ({"firstName": "TestUser_firstName", "login": "login", "password": "password"},  "missing 'lastName'"),
    ({"lastName": "TestUser_lastName", "login": "login", "password": "password"},  "missing 'firstName'"),
    ({"firstName": "TestUser_firstName", "lastName": "TestUser_lastName", "password": "password"},  "missing 'login'"),
    ({"firstName": "TestUser_firstName", "lastName": "TestUser_lastName", "login": "login",},  "missing 'password'"),
    ({"firstName": 123, "lastName": 123, "login": 123, "password": 123},  "invalid type of fields"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_register_contract_validation_error(api, openapi_validator, payload, description):
    logger.info("[REGISTER][NEGATIVE] invalid payload")
    
    # Act
    with allure.step(f"Попытка зарегистрироваться с данными: {description}"):
        resp = api.register(payload)
        allure.attach(str(payload), name="Invalid login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/login success")
def test_login_contract_success(api, openapi_validator):
    logger.info("[LOGIN][POSITIVE] valid payload")
    
    # Arrange
    payload = {
        "firstName": "TestUser_firstName",
        "lastName": "TestUser_lasttName",
        "login": "TestUser_login",
        "password": "TestUser_password"
    }

    with allure.step("Регистрация"):
        api.register(payload)
        allure.attach(str(payload), name="User's data", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Авторизация"):
        resp = api.login({"login": payload["login"], "password": payload["password"]})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 200, f"Ожидалось 200, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/login wrong credentials")
def test_wrong_login_contract(api, openapi_validator):
    logger.info("[LOGIN][POSITIVE] wrong credentials")
    
    # Arrange
    payload = {
        "firstName": "TestUser_firstName",
        "lastName": "TestUser_lasttName",
        "login": "TestUser_login",
        "password": "TestUser_password"
    }

    with allure.step("Регистрация"):
        api.register(payload)
        allure.attach(str(payload), name="User's data", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Авторизация"):
        resp = api.login({"login": payload["login"], "password": "wrong_password"})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


INVALID_PAYLOADS = [
    ({"password": "password"},  "missing 'login'"),
    ({"login": "login",},  "missing 'password'"),
    ({"login": 123, "password": 123},  "invalid type of fields"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/login invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_login_validation_error_contract(api, openapi_validator, payload, description):
    logger.info("[LOGIN][NEGATIVE] invalid payload")
    
    # Act
    with allure.step(f"Попытка авторизоваться с данными: {description}"):
        resp = api.login(payload)
        allure.attach(str(payload), name="Invalid login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_create_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[CREATE CAT][NEGATIVE] Unauthorized")
    
    # Arrange
    cat_payload = {"name": generate_unique_cat_name(), "age": 2, "breed": "Test"}
    
    # Act
    with allure.step(f"Попытка создания кота"):
        resp = api.create_cat(cat_payload)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_delete_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[DELETE CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step(f"Попытка удаления кота"):
        resp = api.delete_cat(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_cat_by_Id_unauthorized_contract(api, openapi_validator, auth_token):
    logger.info("[GET CAT BY ID][POSITIVE] do not required to be authorized")
    
    # Arrange
    cat_payload = {"name": generate_unique_cat_name(), "age": 2, "breed": "Test"}
    with allure.step(f"Создаем кота"):
        create_resp = api.create_cat(cat_payload, token=auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Попытка получения кота по Id"):
        get_resp = api.get_cat_by_id(cat_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_all_cats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET ALL CATS][POSITIVE] do not required to be authorized")
    
    # Act
    with allure.step("Попытка получения всех котов"):
        get_resp = api.get_all_cats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_patch_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] Unauthorized")
    
    # Arrange
    patch_payload = {"name": "TestCat_UpdatedName", "age": 5}

    # Act
    with allure.step("Попытка обновления данных"):
        patch_resp = api.patch_cat(1, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)



@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_adopt_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[ADOPT CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка обновления данных кота о новом ладельце"):
        patch_resp = api.adopt_cat(1, {"userId": 1})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_create_user_unauthorized_contract(api, openapi_validator):
    logger.info("[CREATE USER][NEGATIVE] Unauthorized")
    
    # Arrange
    payload = generate_unique_user_payload()

    # Act
    with allure.step("Попытка создания нового пользователя"):
        create_resp = api.create_user(payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert create_resp.status_code == 401, f"Ожидалось 401, получено {create_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(create_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_users_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USERS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения всех пользователей"):
        get_resp = api.get_all_users()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_user_by_Id_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USER BY ID][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения пользователя по Id"):
        get_resp = api.get_user_by_id(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_adopted_cats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения котов пользователя"):
        get_resp = api.get_adopted_cats_by_userId(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_delete_user_unauthorized_contract(api, openapi_validator):
    logger.info("[DELETE USER][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка удаления пользователя"):
        delete_resp = api.delete_user(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert delete_resp.status_code == 401, f"Ожидалось 401, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_summary_unauthorized_contract(api, openapi_validator):
    logger.info("[GET SUMMARY][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики"):
        stats_resp = api.get_summary_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_breed_stats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET BREED STATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики"):
        stats_resp = api.get_stats_by_breed()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_adopters_stats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET ADOPTERS STATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики"):
        stats_resp = api.get_adopters_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stats_resp)
