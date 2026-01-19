import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Update Cat")
def test_update_cat_success(api_base_url):
    """Позитивный тест: обновление кота"""
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 2, "breed": "British"}

    with allure.step("Создаём кота"):
        create_resp = requests.post(api_base_url, json=payload)
        assert create_resp.status_code == 201
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Обновляем данные кота"):
        new_name = generate_unique_cat_name()
        update_data = {"name": new_name, "age": 3}
        update_resp = requests.patch(f"{api_base_url}/{cat_id}", json=update_data)
        assert update_resp.status_code == 200
        updated = update_resp.json()["data"]
        assert updated["name"] == new_name
        assert updated["age"] == 3
        assert updated["breed"] == "British"

@allure.feature("Cats CRUD")
@allure.story("Update Cat")
def test_update_cat_duplicate_name(api_base_url):
    """Негативный тест: обновление с конфликтом имени"""
    with allure.step("Создаём двух котов"):
        name1 = generate_unique_cat_name()
        name2 = generate_unique_cat_name()
        resp1 = requests.post(api_base_url, json={"name": name1, "age": 1, "breed": "A"})
        resp2 = requests.post(api_base_url, json={"name": name2, "age": 1, "breed": "B"})
        assert resp1.status_code == 201
        assert resp2.status_code == 201
        cat1 = resp1.json()["data"]
        cat2 = resp2.json()["data"]

    with allure.step("Попытка переименовать cat2 в имя cat1"):
        update_resp = requests.patch(f"{api_base_url}/{cat2['id']}", json={"name": name1})
        assert update_resp.status_code == 409