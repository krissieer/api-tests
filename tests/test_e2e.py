import pytest
import allure
import requests
from utils.helpers import generate_unique_cat_name, assert_cat_response

@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Full lifecycle of a cat")
def test_cat_full_lifecycle(api_base_url):
    """Создание → обновление → удаление → проверка отсутствия"""
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "E2E"}

    new_name = generate_unique_cat_name()
    update_data = {"name": new_name, "age": 5, "breed": "Updated E2E"}

    # Act
    with allure.step("Cоздаем кота"):
        create_resp = requests.post(api_base_url,json=payload)
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Обновляем данные кота"):
        update_resp = requests.patch(f"{api_base_url}/{cat_id}", json=update_data)
       
    with allure.step("Удаляем кота"):
        delete_resp = requests.delete(f"{api_base_url}/{cat_id}")

    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert create_resp.status_code == 201

    with allure.step("Проверяем успешное обновление данных"):
        assert update_resp.status_code == 200
        updated = update_resp.json()["data"]
        assert_cat_response(updated, new_name, 5, "Updated E2E")

    with allure.step("Проверяем удаление кота"):
        assert delete_resp.status_code == 204
        get_resp = requests.get(f"{api_base_url}/{cat_id}")
        assert get_resp.status_code == 404