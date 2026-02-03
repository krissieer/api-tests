import pytest
import allure
from utils.helpers import generate_unique_cat_name
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats")
def test_create_cat_contract(api, openapi_validator):
    logger.info("[CREATE CAT][POSITIVE] valid payload")
    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 3, "breed": "POST",}
    
    # Act
    with allure.step("Создаём нового кота"):
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(create_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats")
def test_create_cat_duplicate_name(api, openapi_validator):
    logger.info("[CREATE CAT][NEGATIVE] duplicate name")
    # Arrange
    name = generate_unique_cat_name()
    payload1 = {"name": name, "age": 2, "breed": "Persian"}
    payload2 = {"name": name, "age": 4, "breed": "Maine Coon"}
    
    # Act
    with allure.step("Создаём первого кота"):
        resp1 = api.create_cat(payload1)
        allure.attach(str(payload1), name="Payload", attachment_type=allure.attachment_type.JSON)
    with allure.step("Пытаемся создать второго с тем же именем"):
        resp2 = api.create_cat(payload2)
        allure.attach(str(payload2), name="Payload", attachment_type=allure.attachment_type.JSON)
        
    # Assert
    with allure.step("Проверяем HTTP-статус при создании первого кота"):
        assert resp1.status_code == 201, f"Ожидалось 201, получено {resp1.status_code}"
    with allure.step("Проверяем ошибку при создании кота с дублирующимся именем"):
        assert resp2.status_code == 409, f"Ожидалось 409, получено {resp2.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp1)
        openapi_validator.validate_response(resp2)

INVALID_PAYLOADS = [
    ({"age": 3, "breed": "B"}, "missing 'name'"),
    ({"name": "TestCat_", "breed": "B"}, "missing 'age'"),
    ({"name": "TestCat_", "age": 3}, "missing 'breed'"),
    ({"name": "TestCat_", "age": "old", "breed": "B"}, "invalid type of 'age'"),
    ({"name": 5, "age": 5, "breed": 5}, "invalid type of 'name' and 'breed'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_cat_invalid_contract(api, openapi_validator, payload, description):
    logger.info("[CREATE CAT][NEGATIVE] duplicate name invalid payload")
    
    # Act
    with allure.step(f"Отправляем POST с недопустимым payload: {description}"):
        resp = api.create_cat(payload)
        allure.attach(str(payload), name="Invalid Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats")
def test_get_all_cats_contract(api, openapi_validator):
    logger.info("[GET CATS][POSITIVE] Get all cats")

    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 10, "breed": "GET",}
    with allure.step("Создаём нового кота"):
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    
    # Act
    with allure.step("Запрашиваем всех котов"):
        get_resp = api.get_all_cats()
        allure.attach(str(get_resp.json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats/{id}")
def test_get_cat_by_id_contract(api, openapi_validator):
    logger.info("[GET CAT][POSITIVE] Get cat by valid Id")

    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 5, "breed": "GET_ID"}

    with allure.step("Создаём нового кота"):
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]
    
    # Act
    with allure.step("Запрашиваем кота по ID"):
        get_resp = api.get_cat_by_id(cat_id)
        allure.attach(str(get_resp.json()), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats/{id} invalid ID")
@pytest.mark.parametrize("ID, expected_status, description", 
    [(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")],
    ids=["nonexistent id", "invalid id format"])
def test_get_by_invalid_ID_contract(api, openapi_validator, ID, expected_status, description):
    logger.info("[GET CAT][NEGATIVE] Get cat by invalid Id")

    # Act
    with allure.step(f"Запрашиваем по некорректному ID: {description}"):
        get_resp = api.get_cat_by_id(ID)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
       assert get_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id}")
def test_get_cat_by_id_contract(api, openapi_validator):
    logger.info("[DELETE CAT][POSITIVE] Delete cat by valid Id")
    
    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 7, "breed": "DELETE",}
    with allure.step("Создаём нового кота"):
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]
    
    # Act
    with allure.step("Удаляем кота"):
        delete_resp = api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id} invalid ID")
@pytest.mark.parametrize("ID, expected_status, description", 
[(9999, 404, "nonexistent id"), ("abc", 400, "invalid id format")])
def test_delete_invalid_ID_contract(api, openapi_validator, ID, expected_status, description):
    logger.info("[DELETE CAT][NEGATIVE] Delete cat by invalid Id")

    # Act
    with allure.step(f"Удаляем по некорректному ID: {description}"):
        delete_resp = api.delete_cat(ID)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
       assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Boundary: name length")
@pytest.mark.parametrize("name", ["", "A", " "], ids=["empty name", "one_char name", "space"])
def test_create_cat_name_too_short(api, openapi_validator, name):
    logger.info("[CREATE CAT][NEGATIVE] borderline name length")
    
    # Arrange
    payload = {"name": name, "age": 2, "breed": "Boundary"}

    # Act
    with allure.step(f"Отправляем POST с именем: '{name}'"):
        response = api.create_cat(payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert response.status_code == 400, f"Ожидалось 400, получено {response.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(response)
    

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Boundary: age values")
@pytest.mark.parametrize("age, expected_status", [(-1, 400), (0, 201), (1, 201)], ids=["-1", "0", "1"])
def test_create_cat_age_boundary(api, openapi_validator, age, expected_status):
    logger.info("[CREATE CAT][POSITIVE/NEGATIVE] borderline age values")
    
    # Arrange 
    payload = {"name": generate_unique_cat_name(), "age": age, "breed": "Boundary"}
    
    # Act
    with allure.step(f"Отправляем POST с возрастом: {age}"):
        resp = api.create_cat(payload)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
        assert resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(resp)