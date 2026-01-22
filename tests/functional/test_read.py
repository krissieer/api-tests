import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Get Cats")
def test_get_all_cats(api_base_url):
    """Позитивный тест: получение списка всех котов"""
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "Bengal"}

    
    with allure.step("Создаём временного кота"):
        create_resp = requests.post(api_base_url, json=payload)
    with allure.step("Получаем список всех котов"):
        all_resp = requests.get(api_base_url)

    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert create_resp.status_code == 201
        cat_id = create_resp.json()["data"]["id"]

    with allure.step("Проверяем корректность списка котов"):
        assert all_resp.status_code == 200
        cats = all_resp.json()["data"]
        assert isinstance(cats, list)
        assert len(cats) >= 1
        assert any(cat["id"] == cat_id for cat in cats), \
            "Созданный кот не найден в списке"

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Get Cat by ID")
def test_get_cat_by_id_success(api_base_url):
    """Позитивный тест: получение кота по ID"""
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 5, "breed": "Sphynx"}
    with allure.step("Создаём кота"):
        create_resp = requests.post(api_base_url, json=payload)

    # Act
    with allure.step("Запрашиваем кота по ID"):
        cat_id = create_resp.json()["data"]["id"]
        get_resp = requests.get(f"{api_base_url}/{cat_id}")
        
    # Assert 
    with allure.step("Проверяем корректность ответа"):
        assert create_resp.status_code == 201
        assert get_resp.status_code == 200
        data = get_resp.json()["data"]
        assert data["id"] == cat_id
        assert_cat_response(data, name, 5, "Sphynx")

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Get Cat by ID")
def test_get_cat_by_invalid_id(api_base_url):
    """Негативный тест: запрос несуществующего ID"""
    # Arrange
    invalid_id = 999999
    
    # Act
    with allure.step("Запрашиваем несуществующий ID"):
        response = requests.get(f"{api_base_url}/invalid_id")

    # Assert 
    with allure.step("Проверяем код ошибки"):
        assert response.status_code == 400