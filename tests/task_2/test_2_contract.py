import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload
import utils.openapi_validator

@pytest.mark.task2
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users")
def test_create_user_contract(api, openapi_validator):
    # Arrange
    payload = generate_unique_user_payload()

    # Act
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert create_resp.status_code == 201
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(create_resp)

INVALID_PAYLOADS = [
    ({"lastName": "Test_user"}, "missing 'firstName'"),
    ({"firstName": "Test_user"}, "missing 'lastName'"),
    ({"firstName": 1, "lastName": 1}, "invalid type of 'firstName' and 'lastName'"),
    ({}, "empty payload")]
@pytest.mark.task2
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_user_invalid_contract(api, openapi_validator, payload, description):
    # Act
    with allure.step(f"Отправляем POST с недопустимым payload: {description}"):
        resp = api.create_user(payload)
        allure.attach(str(payload), name="Invalid Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)

INVALID_PAYLOADS = [
    ({"firstName": "  ", "lastName": "  "}, "empty fields"),
    ({"firstName": "A", "lastName": "A"}, "too short 'firstName' and 'lastName'"),
    ({"firstName": "", "lastName": ""}, "empty fields")]
@pytest.mark.task2
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Boundary: user's name length")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_cat_namesboundary_contract(api, openapi_validator, payload, description):
    # Act
    with allure.step(f"Отправляем POST-запрос: {description}"):
        resp = api.create_user(payload)
        allure.attach(str(payload), name="Invalid user's name", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("GET/users")
def test_get_all_users_contract(api, openapi_validator):
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)

    # Act
    with allure.step("Запрашиваем всех пользователей"):
        get_resp = api.get_all_users()

     # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("GET/users/{id}")
def test_get_user_by_id_contract(api, openapi_validator):
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Запрашиваем пользователя по ID"):
        get_resp = api.get_user_by_id(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("GET/users/{id} invalid format")
@pytest.mark.parametrize("ID, expected_status, description", 
[(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_get_user_invalid_id_format_contract(api, openapi_validator, ID, expected_status, description):
    # Act
    with allure.step(f"Запрашиваем по некорректному ID: {description}"):
        get_resp = api.get_user_by_id(ID)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert get_resp.status_code == expected_status
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)



@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_contract(api, openapi_validator):
    # Arrange
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        create_user_resp = api.create_user(payload_user)
    patch_payload =  {"userId": create_user_resp.json()["id"]}
    
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 7, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
    cat_id = create_cat_resp.json()["id"]
    
    # Act
    with allure.step("Обновляем данные"):
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid cat's id format")
@pytest.mark.parametrize("catId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_patch_cat_invalid_catid_contract(api, openapi_validator, catId, expected_status, description):
    # Arrange
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(payload_user)
    patch_payload = {"userId": create_user.json()["id"]}

    # Act
    with allure.step(f"Запрашиваем с некорректным ID: {description}"):
        patch_resp = api.adopt_cat(catId, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == expected_status
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid user's Id format")
@pytest.mark.parametrize("userId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_patch_cat_invalid_userid_contract(api, openapi_validator, userId, expected_status, description):
    # Arrange
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 2, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"userId": userId}

    # Act
    with allure.step(f"Запрашиваем с некорректным ID: {description}"):
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == expected_status
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)



@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}")
def test_patch_cat_contract(api, openapi_validator):
    # Arrange
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 3, "breed": "Patch"}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
    cat_id = create_cat_resp.json()["id"]
    
    patch_payload = {
        "name": "TestCat_UpdatedName",
        "age": 5,
        "breed": "Updated Breed",
        "history": "Updated history",
        "description": "Updated description"
    }

    # Act
    with allure.step("Обновляем данные"):
        patch_resp = api.patch_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid cat's id format")
@pytest.mark.parametrize("catId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_patch_cat_not_found_contract(api, openapi_validator, catId, expected_status, description):
    # Arrange
    patch_payload = {"name": "UpdatedName"}

    # Act
    with allure.step(f"Обновляем данные с некорректным ID: {description}"):
        patch_resp = api.patch_cat(catId, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == expected_status
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)

@pytest.mark.task2
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid payload")
def test_patch_cat_invalid_payload_contract(api, openapi_validator):
    # Arrange
    payload_cat = {"name": generate_unique_cat_name(), "age": 2, "breed": "Patch"}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"name": "  ", "age": -8, "breed": " "}
    
    # Act
    with allure.step(f"Отправляем PATCH-запрос с невалидным payload"):
        resp = api.patch_cat(cat_id, patch_payload)
        allure.attach(str(patch_payload), name="invalid payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)

@pytest.mark.contract
@pytest.mark.task2
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} duplicate name")
def test_patch_cat_duplicate_name_contract(api, openapi_validator):
    # Arrange
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 2, "breed": "Patch"}
    with allure.step("Создаём 1го кота"):
        create_cat1_resp = api.create_cat(payload_cat)
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 1, "breed": "Patch"}
    with allure.step("Создаём 2го кота"):
        create_cat2_resp = api.create_cat(payload_cat)
    cat_id = create_cat2_resp.json()["id"]

    patch_payload = {"name": name}
    # Act
    with allure.step(f"Обновляем имя 2го кота на имя 1го кота"):
        patch_resp = api.patch_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == 409
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)