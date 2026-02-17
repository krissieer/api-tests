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
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
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
        logger.info(f"Создание пользователя с недопустимым payload: {description}")
        resp = api.create_user(payload)
        logger.debug(f"Payload: {payload}")
        allure.attach(str(payload), name="Invalid Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
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
    with allure.step(f"Отправляем POST-запрос с недопустимым именем пользователя: {description}"):
        logger.info(f"Создание пользователя с недопустимым именем: {description}")
        resp = api.create_user(payload)
        logger.debug(f"Payload: {payload}")
        allure.attach(str(payload), name="Invalid user's name", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users")
def test_get_all_users_contract(api, openapi_validator):
    logger.info("[GET USERS][POSITIVE] Get all users")
    
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Запрашиваем всех пользователей"):
        logger.info(f"Запрашиваем всех пользователей")
        get_resp = api.get_all_users()
        logger.debug(f"Список пользователей: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="All users", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}")
def test_get_user_by_id_contract(api, openapi_validator):
    logger.info("[GET USER][POSITIVE] Get user by valid Id")
    
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="created user", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Запрашиваем пользователя по ID"):
        logger.info(f"Запрашиваем пользователя по ID: {user_id}")
        get_resp = api.get_user_by_id(user_id)
        logger.debug(f"Найденный пользователей: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="gotten user", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id} invalid format")
@pytest.mark.parametrize("ID, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_get_user_invalid_id_format_contract(api, openapi_validator, ID, expected_status):
    logger.info("[GET USER][NEGATIVE] Get user by invalid Id")

    # Act
    with allure.step(f"Запрашиваем по некорректному ID: {ID}"):
        logger.info(f"Запрашиваем по некорректному ID: {ID}")
        get_resp = api.get_user_by_id(ID)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id}")
def test_delete_user_contract(api, openapi_validator):
    logger.info("[DELETE USER][POSITIVE] Delete user by valid Id")
    
    # Arrange
    payload = generate_unique_user_payload()
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_resp = api.delete_user(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} invalid user's id format")
@pytest.mark.parametrize("userId, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_delete_user_invalid_id_contract(api, openapi_validator, userId, expected_status):
    logger.info("[DELETE USER][NEGATIVE] Delete user by invalid Id")
    
    # Act
    with allure.step(f"Удаляем пользователя с некорректным ID: {userId}"):
        logger.info(f"Удаляем пользователя с некорректным ID: {userId}")
        delete_resp = api.delete_user(userId)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_contract(api, openapi_validator):
    logger.info("[PATCH CAT][POSITIVE] adopt cat valid payload")
    
    # Arrange
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание нового пользователя: {payload_user}")
        create_user_resp = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    patch_payload =  {"userId": create_user_resp.json()["id"]}
    
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 7, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]
    
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        logger.info("Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, patch_payload)
        logger.debug(f"Обновленные данные кота: {patch_resp.json()}")

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid cat's id format")
@pytest.mark.parametrize("catId, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_patch_cat_invalid_catid_contract(api, openapi_validator, catId, expected_status):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid cat's id")
    
    # Arrange
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание нового пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    patch_payload = {"userId": create_user.json()["id"]}

    # Act
    with allure.step(f"Запрашиваем с некорректным cat_Id: {catId}"):
        logger.info(f"Запрашиваем с некорректным cat_Id: {catId}")
        patch_resp = api.adopt_cat(catId, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid user's Id format")
@pytest.mark.parametrize("userId, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_patch_cat_invalid_userid_contract(api, openapi_validator, userId, expected_status):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid user's id")
    
    # Arrange
    name = generate_unique_cat_name()
    payload_cat = {"name": name, "age": 2, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"userId": userId}

    # Act
    with allure.step(f"Запрашиваем с некорректным user_Id: {userId}"):
        logger.info(f"Запрашиваем с некорректным user_Id: {userId}")
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt already adopted cat")
def test_adopt_adopted_cat_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] adopt already adopted cat")
    
    # Arrange
    payload_cat = {"name": generate_unique_cat_name(), "age": 2, "breed": "Patch",}
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание нового пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User_1", attachment_type=allure.attachment_type.JSON)
    patch_payload = {"userId": create_user.json()["id"]}

    with allure.step("Обновляем данные кота о владельце"):
        logger.info("Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    payload_user_2 = generate_unique_user_payload()
    with allure.step("Создаём 2го пользователя"):
        logger.info(f"Создание 2го пользователя: {payload_user_2}")
        create_user_2 = api.create_user(payload_user_2)
        allure.attach(str(payload_user_2), name="User_2", attachment_type=allure.attachment_type.JSON)
    patch_payload_2 = {"userId": create_user_2.json()["id"]}

    # Act
    with allure.step("Пытаемся обновить данные кота о владельце на 2го пользователя"):
        logger.info("Пытаемся обновить данные кота о владельце на 2го пользователя")
        faild_adopt_resp = api.adopt_cat(cat_id, patch_payload_2)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {faild_adopt_resp.status_code}")
        assert faild_adopt_resp.status_code == 400, f"Ожидалось 400, получено {faild_adopt_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
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
        logger.info(f"Создание нового кота: {payload_cat}")
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
        logger.info("Обновляем данные кота")
        patch_resp = api.patch_cat(cat_id, patch_payload)
        logger.debug(f"Новые данные: {patch_payload}")
        allure.attach(str(patch_payload), name="New data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid cat's id format")
@pytest.mark.parametrize("catId, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_patch_cat_not_found_contract(api, openapi_validator, catId, expected_status):
    logger.info("[PATCH CAT][NEGATIVE] update cat with invalid id")
    
    # Arrange
    patch_payload = {"name": "UpdatedName"}

    # Act
    with allure.step(f"Обновляем данные с некорректным cat_Id: {catId}"):
        logger.info(f"Попытка обновления данных кота с некорректным cat_Id: {catId}")
        patch_resp = api.patch_cat(catId, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid payload")
def test_patch_cat_invalid_payload_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] update cat with invalid payload")
    
    # Arrange
    payload_cat = {"name": generate_unique_cat_name(), "age": 2, "breed": "Patch"}
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"name": "  ", "age": -8, "breed": " "}
    
    # Act
    with allure.step(f"Отправляем PATCH-запрос с невалидным payload"):
        logger.info(f"Отправляем PATCH-запрос с невалидным payload")
        resp = api.patch_cat(cat_id, patch_payload)
        logger.debug(f"Невалидные данные: {patch_payload}")
        allure.attach(str(patch_payload), name="invalid payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
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
        logger.info(f"Создание 1го кота: {payload_cat_1}")
        create_cat1_resp = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    
    payload_cat_2 = {"name": generate_unique_cat_name(), "age": 1, "breed": "Patch"}
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создание 2го кота: {payload_cat_2}")
        create_cat2_resp = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat2_resp.json()["id"]

    patch_payload = {"name": name}
    # Act
    with allure.step(f"Обновляем имя 2го кота на имя 1го кота"):
        logger.info(f"Попытка обновить имя 2го кота на имя 1го кота")
        patch_resp = api.patch_cat(cat_id, patch_payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 409, f"Ожидалось 409, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)



@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats")
def test_get_adopted_cats_by_userId_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][POSITIVE] get adopted cats by user")
    
    # Arrange 
    payload = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload}")
        create_user = api.create_user(payload)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat_1 = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём 1го кота"):
        logger.info(f"Создание 1го кота: {payload_cat_1}")
        create_cat_1 = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    cat_1_id = create_cat_1.json()["id"]

    payload_cat_2 = {"name": generate_unique_cat_name(), "age": 1, "breed": "Test"}
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создание 2го кота: {payload_cat_2}")
        create_cat_2 = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_2_id = create_cat_2.json()["id"]

    with allure.step("Обновляем данные о владельце 1ой кошки"):
        logger.info("Обновляем данные о владельце 1ой кошки")
        patch_1_resp = api.adopt_cat(cat_1_id, adopt_payload)
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_2_resp = api.adopt_cat(cat_2_id, adopt_payload)

    # Act
    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user_cats_resp = api.get_adopted_cats_by_userId(user_id)
        logger.debug(f"Список кошек пользователя: {user_cats_resp.json()}")
        allure.attach(str(user_cats_resp.json()), name="User's cats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {user_cats_resp.status_code}")
        assert user_cats_resp.status_code == 200, f"Ожидалось 200, получено {user_cats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(user_cats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats")
@pytest.mark.parametrize("userId, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_get_adopted_cats_by_invalid_userId_contract(api, openapi_validator, userId, expected_status):
    logger.info("[GET USER'S CATS][NEGATIVE] get cats by invalid userID")
    
    # Act
    with allure.step(f"Получаем данные пользователя с некорректным ID: {userId}"):
        logger.info(f"Получаем данные пользователя с некорректным ID: {userId}")
        user_cats_resp = api.get_adopted_cats_by_userId(userId)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {user_cats_resp.status_code}")
        assert user_cats_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {user_cats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(user_cats_resp)