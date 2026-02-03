import pytest
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.integration
@allure.feature("Integration")
def test_cat_list_length_changes(api):
    logger.info("[Integration] changing amount of cats in DB")
    
    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "Integration"}

    # Act
    with allure.step("Получаем исходный список котов"):
        initial_resp = api.get_all_cats()
        allure.attach(str(initial_resp.json()), name="initial cat list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём нового кота"):
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    with allure.step("Получаем список котов после добавления"):
        after_create_resp = api.get_all_cats()
        allure.attach(str(after_create_resp.json()), name="after addition cat list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Удаляем созданного кота"):
        delete_resp = api.delete_cat(cat_id)

    with allure.step("Получаем список котов после удаления"):
        final_resp = api.get_all_cats()
        allure.attach(str(final_resp.json()), name="after deleting cat list", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step(f"Проверяем начальное количество котов: {len(initial_resp.json())}"):
        initial_count = len(initial_resp.json())

    with allure.step("Проверяем, что после добавления количество котов увеличилось"):
        new_count = len(after_create_resp.json())
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"

    with allure.step(f"Проверяем, что после удаления количество вернулось к исходному: {len(final_resp.json())}"):
        final_count = len(final_resp.json())
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"


@pytest.mark.integration
@allure.feature("Integration")
def test_cat_create_get_delete(api):
    logger.info("[Integration] Checking accessibility after adding and deleting")
    
    # Arrange
    payload = {"name": generate_unique_cat_name(), "age": 4,  "breed": "Integration",}

    # Act
    with allure.step("Создаём кота"):
        cat_id = api.create_cat(payload).json()["id"]
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    with allure.step("Проверяем его наличие после добавления"):
        get_resp = api.get_cat_by_id(cat_id)
        allure.attach(str(get_resp.json()), name="cat", attachment_type=allure.attachment_type.JSON)        
    with allure.step("Удаляем кота"):
        api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем, что кот после добавления доступен по ID: 200"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем, что кот исчез"):
        get_deleted = api.get_cat_by_id(cat_id)
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"

@pytest.mark.integration
@allure.feature("Integration")
def test_invalid_cat_not_saved(api):
    logger.info("[Integration] Checking the immutability of the DB when trying to add invalid cat")
    
    # Arrange
    payload = {"name": "A", "age": -1, "breed": "Integration",}

    # Act
    with allure.step("Получаем исходный список котов"):
        initial_resp = api.get_all_cats()
        allure.attach(str(initial_resp.json()), name="cats", attachment_type=allure.attachment_type.JSON)  
    
    with allure.step("Добавляем кота с невалидными данными"):
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Invalid payload", attachment_type=allure.attachment_type.JSON)          

    with allure.step("Получаем список после попытки добавленияя"):
        after_resp = api.get_all_cats()
        allure.attach(str(after_resp.json()), name="cats after trying addition", attachment_type=allure.attachment_type.JSON)  

    # Assert
    with allure.step("Сравниваем количество до и после попытки добавления"):
        initial_count = len(initial_resp.json())
        after_count = len(after_resp.json())
        assert after_count == initial_count, f"Ожидалось {initial_count}, получено {after_count}"


@pytest.mark.integration
@allure.feature("Integration")
def test_multiple_cat_creation(api):
    logger.info("[Integration] Checking for multiple cat creation")    
    
    # Arrange 
    payloads = [
        {
            "name": generate_unique_cat_name(),
            "age": 1,
            "breed": "Integration",
        }
        for _ in range(3)
    ]
    created_ids = []

    # Act
    with allure.step("Создаём котов и добавляем их Id в список"):
        for payload in payloads:
            created_cat = api.create_cat(payload).json()["id"]
            created_ids.append(created_cat)

    with allure.step("Получаем всех котов и их Id"):
        all_cats= api.get_all_cats().json()
        all_cat_ids = [cat["id"] for cat in all_cats]

    # Assert
    with allure.step("Сравниваем Id созданных и полученных из БД котов"):
        for cat_id in created_ids:
            assert cat_id in all_cat_ids