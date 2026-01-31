import pytest
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response

# проверка взаимодействия с БД
@pytest.mark.task1
@pytest.mark.integration
@allure.feature("Integration")
def test_cat_list_length_changes(api):
    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "Integration"}

    # Act
    with allure.step("Получаем исходный список котов"):
        initial_resp = api.get_all_cats()

    with allure.step("Создаём нового кота"):
        create_resp = api.create_cat(payload)
    cat_id = create_resp.json()["id"]

    with allure.step("Получаем список котов после добавления"):
        after_create_resp = api.get_all_cats()

    with allure.step("Удаляем созданного кота"):
        delete_resp = api.delete_cat(cat_id)

    with allure.step("Получаем список котов после удаления"):
        final_resp = api.get_all_cats()

    # Assert
    with allure.step("Проверяем начальное количество котов"):
        initial_count = len(initial_resp.json())

    with allure.step("Проверяем, что после добавления количество котов увеличилось"):
        new_count = len(after_create_resp.json())
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"

    with allure.step("Проверяем, что количество вернулось к исходному"):
        final_count = len(final_resp.json())
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"

@pytest.mark.task1
@pytest.mark.integration
@allure.feature("Integration")
def test_cat_create_get_delete(api):
    # Arrange
    payload = {"name": generate_unique_cat_name(), "age": 4,  "breed": "Integration",}

    # Act
    with allure.step("Создаём кота"):
        create_resp = api.create_cat(payload)
        cat_id = create_resp.json()["id"]

    with allure.step("Проверяем его наличие после добавления"):
        get_resp = api.get_cat_by_id(cat_id)
    
    with allure.step("Удаляем кота"):
        api.delete_cat(cat_id)

    with allure.step("Проверяем его наличие после добавления"):
        get_deleted = api.get_cat_by_id(cat_id)

    # Assert
    with allure.step("Проверяем, что кот после добавления доступен по ID"):
        assert get_resp.status_code == 200
    with allure.step("Проверяем, что кот исчез"):
        assert get_deleted.status_code == 404

@pytest.mark.task1
@pytest.mark.integration
@allure.feature("Integration")
def test_invalid_cat_not_persisted(api):
    # Arrange
    payload = {"name": "A", "age": -1, "breed": "Integration",}

    # Act
    with allure.step("Получаем исходный список котов"):
        initial_resp = api.get_all_cats()
    
    with allure.step("Добавляем котас невалидными данными"):
        create_resp = api.create_cat(payload)

    with allure.step("Получаем список после попытки добавленияя"):
        after_resp = api.get_all_cats()
    
    # Assert
    with allure.step("Сравниваем количество до и после попытки добавления"):
        initial_count = len(initial_resp.json())
        after_count = len(after_resp.json())
        assert after_count == initial_count

@pytest.mark.task1
@pytest.mark.integration
@allure.feature("Integration")
def test_multiple_cat_creation(api):
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
    for payload in payloads:
        response = api.create_cat(payload)
        created_ids.append(response.json()["id"])

    all_cats_response = api.get_all_cats()
    all_cat_ids = [cat["id"] for cat in all_cats_response.json()]

    # Assert
    for cat_id in created_ids:
        assert cat_id in all_cat_ids