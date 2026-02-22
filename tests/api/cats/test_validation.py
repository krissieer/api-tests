import pytest
import allure
from utils.data_builders import generate_unique_cat_name
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("Boundary: name length")
@pytest.mark.parametrize("name", ["", "A", " "], ids=["empty name", "one_char name", "space"])
def test_create_cat_name_too_short(api, openapi_validator, name):
    logger.info("[API] borderline name length")
    
    # Arrange
    payload = {"name": name, "age": 2, "breed": "Boundary"}

    # Act
    with allure.step(f"Отправляем POST с именем: '{name}'"):
        logger.info(f"Попытка создания кота с именем: '{name}'")
        response = api.create_cat(payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {response.status_code}")
        assert response.status_code == 400, f"Ожидалось 400, получено {response.status_code}"
    
    
@pytest.mark.api
@allure.feature("API")
@allure.story("Boundary: age values")
@pytest.mark.parametrize("age, expected_status", [(-1, 400), (0, 201), (1, 201)], ids=["-1", "0", "1"])
def test_create_cat_age_boundary(api, openapi_validator, age, expected_status):
    logger.info("[API] borderline age values")
    
    # Arrange 
    payload = {"name": generate_unique_cat_name(), "age": age, "breed": "Boundary"}
    
    # Act
    with allure.step(f"Отправляем POST с возрастом: {age}"):
        logger.info(f"Попытка создания кота с возрастом: {age}")
        resp = api.create_cat(payload)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {resp.status_code}"

@pytest.mark.api
@allure.feature("API")
def test_invalid_cat_not_saved(api):
    logger.info("[API] Checking the immutability of the DB when trying to add invalid cat")
    
    # Arrange
    payload = {"name": "A", "age": -1, "breed": "API",}

    # Act
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="cats", attachment_type=allure.attachment_type.JSON)  
    
    with allure.step("Добавляем кота с невалидными данными"):
        logger.info(f"Добавляем кота с невалидными данными {payload}")
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Invalid payload", attachment_type=allure.attachment_type.JSON)          

    with allure.step("Получаем список после попытки добавления"):
        logger.info("Список после попытки добавления")
        after_resp = api.get_all_cats()
        logger.debug(f"Список котов: {after_resp.json()}")
        allure.attach(str(after_resp.json()), name="cats after trying addition", attachment_type=allure.attachment_type.JSON)  

    # Assert
    with allure.step("Сравниваем количество до и после попытки добавления"):
        initial_count = len(initial_resp.json())
        after_count = len(after_resp.json())
        logger.info(f"Количество до попытки добавления - {initial_count}, после - {after_count}")
        assert after_count == initial_count, f"Ожидалось {initial_count}, получено {after_count}"
