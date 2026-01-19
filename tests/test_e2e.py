import pytest
import allure
import requests
from utils.helpers import generate_unique_cat_name

@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Full lifecycle of a cat")
def test_cat_full_lifecycle(api_base_url):
    """Создание → обновление → удаление → проверка отсутствия"""
    with allure.step("Cоздаем кота"):
        name = generate_unique_cat_name()
        create_resp = requests.post(api_base_url,json={"name": name, "age": 1, "breed": "E2E"})
        assert create_resp.status_code == 201
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Обновляем данные кота"):
        new_name = generate_unique_cat_name()
        update_data = {"name": new_name, "age": 5, "breed": "Updated E2E"}
        update_resp = requests.patch(f"{api_base_url}/{cat_id}", json=update_data)
       
        assert update_resp.status_code == 200
        updated = update_resp.json()["data"]
        assert updated["name"] == new_name
        assert updated["age"] == 5
        assert updated["breed"] == "Updated E2E"

    with allure.step("Удаляем кота"):
        delete_resp = requests.delete(f"{api_base_url}/{cat_id}")
        assert delete_resp.status_code == 204

    with allure.step("Проверяем, что кот больше не существует"):
        get_resp = requests.get(f"{api_base_url}/{cat_id}")
        assert get_resp.status_code == 404