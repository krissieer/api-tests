import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Create Cat")
def test_create_cat_success(api_base_url):
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 3, "breed": "Siamese"}
    
    with allure.step("Отправляем POST запрос на создание кота"):
        resp = requests.post(api_base_url, json=payload)
        assert resp.status_code == 201
        data = resp.json()["data"]

    with allure.step("Проверяем структуру ответа"):
        assert "id" in data
        assert data["name"] == name
        assert data["age"] == 3
        assert data["breed"] == "Siamese"    

@allure.feature("Cats CRUD")
@allure.story("Create Cat")
def test_create_cat_duplicate_name(api_base_url):
    """Негативный тест: попытка создать кота с дублирующимся именем"""
    name = generate_unique_cat_name()
    
    with allure.step("Создаём первого кота"):
        payload1 = {"name": name, "age": 2, "breed": "Persian"}
        resp1 = requests.post(api_base_url, json=payload1)
        assert resp1.status_code == 201
        cat1_id = resp1.json()["data"]["id"]

    with allure.step("Пытаемся создать второго с тем же именем"):
        payload2 = {"name": name, "age": 4, "breed": "Maine Coon"}
        resp2 = requests.post(api_base_url, json=payload2)
        assert resp2.status_code == 409

