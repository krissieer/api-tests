import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Create Cat")
def test_create_cat_success(api_base_url):
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 3, "breed": "Siamese"}
    
    # Act
    with allure.step("Отправляем POST запрос на создание кота"):
        resp = requests.post(api_base_url, json=payload)
    
    # Assert 
    with allure.step("Проверяем статус ответа"):
        assert resp.status_code == 201
    with allure.step("Проверяем структуру и содержимое ответа"):
        data = resp.json()["data"]
        assert_cat_response(data, name, 3, "Siamese")

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Create Cat")
def test_create_cat_duplicate_name(api_base_url):
    """Негативный тест: попытка создать кота с дублирующимся именем"""
    # Arrange
    name = generate_unique_cat_name()
    payload1 = {"name": name, "age": 2, "breed": "Persian"}
    payload2 = {"name": name, "age": 4, "breed": "Maine Coon"}
    
    # Act
    with allure.step("Создаём первого кота"):
        resp1 = requests.post(api_base_url, json=payload1)
    with allure.step("Пытаемся создать второго с тем же именем"):
        resp2 = requests.post(api_base_url, json=payload2)
        
    # Assert
    with allure.step("Проверяем успешное создание первого кота"):
        assert resp1.status_code == 201
    with allure.step("Проверяем ошибку при создании кота с дублирующимся именем"):
        assert resp2.status_code == 409


