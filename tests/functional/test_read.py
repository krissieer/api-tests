import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Get Cats")
def test_get_all_cats(api_base_url):
    """Позитивный тест: получение списка всех котов"""
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "Bengal"}

    with allure.step("Создаём временного кота"):
        create_resp = requests.post(api_base_url, json=payload)
        assert create_resp.status_code == 201
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Получаем список всех котов"):
        all_resp = requests.get(api_base_url)
        assert all_resp.status_code == 200
        cats = all_resp.json()["data"]
        assert isinstance(cats, list)
        assert len(cats) >= 1

    with allure.step("Проверяем, что наш кот в списке"):
        found = any(cat["id"] == cat_id for cat in cats)
        assert found, "Созданный кот не найден в списке"

@allure.feature("Cats CRUD")
@allure.story("Get Cat by ID")
def test_get_cat_by_id_success(api_base_url):
    """Позитивный тест: получение кота по ID"""
    with allure.step("Создаём кота"):
        name = generate_unique_cat_name()
        create_resp = requests.post(api_base_url, json={"name": name, "age": 5, "breed": "Sphynx"})
        assert create_resp.status_code == 201
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Запрашиваем по ID"):
        get_resp = requests.get(f"{api_base_url}/{cat_id}")
        assert get_resp.status_code == 200
        data = get_resp.json()["data"]
        assert data["id"] == cat_id
        assert data["name"] == name

@allure.feature("Cats CRUD")
@allure.story("Get Cat by ID")
def test_get_cat_by_invalid_id(api_base_url):
    """Негативный тест: запрос несуществующего ID"""
    with allure.step("Запрашиваем несуществующий ID"):
        response = requests.get(f"{api_base_url}/999999")
        assert response.status_code == 404