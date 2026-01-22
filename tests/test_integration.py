import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name

# проверка взаимодействия с БД

@pytest.mark.integration
@allure.feature("Integration")
@allure.story("State verification")
def test_cat_list_length_changes(api_base_url):
    # Arrange
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "S"}

    # Act
    with allure.step("Получаем исходный список котов"):
        initial_resp = requests.get(api_base_url)

    with allure.step("Создаём нового кота"):
        create_resp = requests.post(api_base_url, json=payload)
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Получаем список котов после добавления"):
        after_create_resp = requests.get(api_base_url)    

    with allure.step("Удаляем созданного кота"):
        delete_resp = requests.delete(f"{api_base_url}/{cat_id}")

    with allure.step("Получаем список котов после удаления"):
        final_resp = requests.get(api_base_url)

    # Assert
    with allure.step("Проверяем начальное количество котов"):
        assert initial_resp.status_code == 200
        initial_data = initial_resp.json()["data"]
        initial_count = len(initial_data)
        allure.attach(str(initial_count), name="Исходное количество", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверяем успешное создание кота"):
        assert create_resp.status_code == 201
        allure.attach(str(cat_id), name="ID созданного кота", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(payload), name="Данные запроса", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем, что количество котов увеличилось на 1"):
        assert after_create_resp.status_code == 200
        new_count = len(after_create_resp.json()["data"])
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"
        allure.attach(str(new_count), name="Количество после создания", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверяем удаление"):
        assert delete_resp.status_code == 204

    with allure.step("Проверяем, что количество вернулось к исходному"):
        assert final_resp.status_code == 200
        final_count = len(final_resp.json()["data"])
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"
        allure.attach(str(final_count), name="Количество после удаления", attachment_type=allure.attachment_type.TEXT)