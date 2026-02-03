import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users")
def test_create_user_contract(api, openapi_validator):
    logger.info("[CREATE USER][POSITIVE] valid payload")

    # Arrange
    payload = generate_unique_user_payload()

    # Act
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(create_resp)


INVALID_PAYLOADS = [
    ({"lastName": "Test_user"}, "missing 'firstName'"),
    ({"firstName": "Test_user"}, "missing 'lastName'"),
    ({"firstName": 1, "lastName": 1}, "invalid type of 'firstName' and 'lastName'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_user_invalid_contract(api, openapi_validator, payload, description):
    logger.info("[CREATE USER][NEGATIVE] invalid payload")

    # Act
    with allure.step(f"Отправляем POST с недопустимым payload: {description}"):
        resp = api.create_user(payload)
        allure.attach(str(payload), name="Invalid Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


INVALID_PAYLOADS = [
    ({"firstName": "  ", "lastName": "  "}, "space"),
    ({"firstName": "A", "lastName": "A"}, "too short 'firstName' and 'lastName'"),
    ({"firstName": "", "lastName": ""}, "empty fields")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Boundary: user's name length")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_cat_namesboundary_contract(api, openapi_validator, payload, description):
    logger.info("[CREATE USER][NEGATIVE] borderline name length")

    # Act
    with allure.step(f"Отправляем POST-запрос: {description}"):
        resp = api.create_user(payload)
        allure.attach(str(payload), name="Invalid user's name", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users")
def test_get_all_users_contract(api, openapi_validator):
    logger.info("[GET USERS][POSITIVE] Get all users")
    
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Запрашиваем всех пользователей"):
        get_resp = api.get_all_users()
        allure.attach(str(get_resp.json()), name="All users", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}")
def test_get_user_by_id_contract(api, openapi_validator):
    logger.info("[GET USER][POSITIVE] Get user by valid Id")
    
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="created user", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Запрашиваем пользователя по ID"):
        get_resp = api.get_user_by_id(user_id)
        allure.attach(str(get_resp.json()), name="gotten user", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id} invalid format")
@pytest.mark.parametrize("ID, expected_status, description", 
[(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_get_user_invalid_id_format_contract(api, openapi_validator, ID, expected_status, description):
    logger.info("[GET USER][NEGATIVE] Get user by invalid Id")

    # Act
    with allure.step(f"Запрашиваем по некорректному ID: {description}"):
        get_resp = api.get_user_by_id(ID)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert get_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id}")
def test_delete_user_contract(api, openapi_validator):
    logger.info("[DELETE USER][POSITIVE] Delete user by valid Id")
    
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Удаляем пользователя"):
        delete_resp = api.delete_user(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} invalid user's id format")
@pytest.mark.parametrize("userId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_delete_user_invalid_id_contract(api, openapi_validator, userId, expected_status, description):
    logger.info("[DELETE USER][NEGATIVE] Delete user by invalid Id")
    
    # Act
    with allure.step(f"Удаляем пользователя с некорректным ID: {description}"):
        delete_resp = api.delete_user(userId)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_contract(api, openapi_validator):
    logger.info("[PATCH CAT][POSITIVE] adopt cat valid payload")
    
    # Arrange
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user_resp = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    patch_payload =  {"userId": create_user_resp.json()["id"]}
    
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 7, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]
    
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid cat's id format")
@pytest.mark.parametrize("catId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_patch_cat_invalid_catid_contract(api, openapi_validator, catId, expected_status, description):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid cat's id")
    
    # Arrange
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    patch_payload = {"userId": create_user.json()["id"]}

    # Act
    with allure.step(f"Запрашиваем с некорректным ID: {description}"):
        patch_resp = api.adopt_cat(catId, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid user's Id format")
@pytest.mark.parametrize("userId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_patch_cat_invalid_userid_contract(api, openapi_validator, userId, expected_status, description):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid user's id")
    
    # Arrange
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 2, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"userId": userId}

    # Act
    with allure.step(f"Запрашиваем с некорректным ID: {description}"):
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt already adopted cat")
def test_patch_cat_invalid_userid_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] adopt already adopted cat")
    
    # Arrange
    payload_cat = {"name": generate_unique_cat_name(), "age": 2, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User_1", attachment_type=allure.attachment_type.JSON)
    patch_payload = {"userId": create_user.json()["id"]}

    with allure.step("Обновляем данные кота о владельце"):
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    payload_user_2 = generate_unique_user_payload()
    with allure.step("Создаём 2го пользователя"):
        create_user_2 = api.create_user(payload_user_2)
        allure.attach(str(payload_user_2), name="User_2", attachment_type=allure.attachment_type.JSON)
    patch_payload_2 = {"userId": create_user_2.json()["id"]}

    # Act
    with allure.step("Пытаемся обновить данные кота о владельце на 2го пользователя"):
        faild_adopt_resp = api.adopt_cat(cat_id, patch_payload_2)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert faild_adopt_resp.status_code == 400, f"Ожидалось 400, получено {faild_adopt_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(faild_adopt_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}")
def test_patch_cat_contract(api, openapi_validator):
    logger.info("[PATCH CAT][POSITIVE] update cat's data")
    
    # Arrange
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 3, "breed": "Patch"}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
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
        allure.attach(str(patch_payload), name="New data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid cat's id format")
@pytest.mark.parametrize("catId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_patch_cat_not_found_contract(api, openapi_validator, catId, expected_status, description):
    logger.info("[PATCH CAT][NEGATIVE] update cat with invalid id")
    
    # Arrange
    patch_payload = {"name": "UpdatedName"}

    # Act
    with allure.step(f"Обновляем данные с некорректным ID: {description}"):
        patch_resp = api.patch_cat(catId, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid payload")
def test_patch_cat_invalid_payload_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] update cat with invalid payload")
    
    # Arrange
    payload_cat = {"name": generate_unique_cat_name(), "age": 2, "breed": "Patch"}
    with allure.step("Создаём нового кота"):
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"name": "  ", "age": -8, "breed": " "}
    
    # Act
    with allure.step(f"Отправляем PATCH-запрос с невалидным payload"):
        resp = api.patch_cat(cat_id, patch_payload)
        allure.attach(str(patch_payload), name="invalid payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} duplicate name")
def test_patch_cat_duplicate_name_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] duplicate name invalid payload")
    
    # Arrange
    name = generate_unique_cat_name()
    payload_cat_1 = {"name": name, "age": 2, "breed": "Patch"}
    with allure.step("Создаём 1го кота"):
        create_cat1_resp = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    
    payload_cat_2 = {"name": generate_unique_cat_name(), "age": 1, "breed": "Patch"}
    with allure.step("Создаём 2го кота"):
        create_cat2_resp = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat2_resp.json()["id"]

    patch_payload = {"name": name}
    # Act
    with allure.step(f"Обновляем имя 2го кота на имя 1го кота"):
        patch_resp = api.patch_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
       assert patch_resp.status_code == 409, f"Ожидалось 409, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)



@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats")
def test_get_adopted_cats_by_userId_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][POSITIVE] get adopted cats by user")
    
    # Arrange 
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(generate_unique_user_payload())
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat_1 = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём 1го кота"):
        create_cat_1 = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    cat_1_id = create_cat_1.json()["id"]

    payload_cat_2 = {"name": generate_unique_cat_name(), "age": 1, "breed": "Test"}
    with allure.step("Создаём 2го кота"):
        create_cat_2 = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_2_id = create_cat_2.json()["id"]

    with allure.step("Обновляем данные о владельце 1ой кошки"):
        patch_1_resp = api.adopt_cat(cat_1_id, adopt_payload)
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        patch_2_resp = api.adopt_cat(cat_2_id, adopt_payload)

    # Act
    with allure.step("Получаем данные пользователя с кошками"):
        user_cats_resp = api.get_adopted_cats_by_userId(user_id)
        allure.attach(str(user_cats_resp.json()), name="User's cats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert user_cats_resp.status_code == 200, f"Ожидалось 200, получено {user_cats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(user_cats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats")
@pytest.mark.parametrize("userId, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_get_adopted_cats_by_invalid_userId_contract(api, openapi_validator, userId, expected_status, description):
    logger.info("[GET USER'S CATS][NEGATIVE] get cats by invalid userID")
    
    # Act
    with allure.step(f"Получаем данные пользователя с некорректным ID: {description}"):
        user_cats_resp = api.get_adopted_cats_by_userId(userId)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert user_cats_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {user_cats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(user_cats_resp)