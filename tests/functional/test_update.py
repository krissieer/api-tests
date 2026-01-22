import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Update Cat")
def test_update_cat_success(api_base_url):
    """Позитивный тест: обновление кота"""
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 2, "breed": "British"}

    new_name = generate_unique_cat_name()
    update_payload = {"name": new_name, "age": 3}

    with allure.step("Создаём кота"):
        create_resp = requests.post(api_base_url, json=payload)
        cat_id = create_resp.json()["data"]["id"]

    # Act
    with allure.step("Обновляем данные кота"):
        update_resp = requests.patch(f"{api_base_url}/{cat_id}", json=update_payload)
        
    # Assert 
    with allure.step("Проверяем структуру и содержимое ответа"):    
        assert create_resp.status_code == 201
        assert update_resp.status_code == 200
        updated = update_resp.json()["data"]
        assert_cat_response(updated, new_name, 3, "British")

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Update Cat")
def test_update_cat_duplicate_name(api_base_url):
    """Негативный тест: обновление с конфликтом имени"""
    # Arrange
    name1 = generate_unique_cat_name()
    name2 = generate_unique_cat_name()
    with allure.step("Создаём двух котов"):
        resp1 = requests.post(api_base_url, json={"name": name1, "age": 1, "breed": "A"})
        resp2 = requests.post(api_base_url, json={"name": name2, "age": 1, "breed": "B"})
        cat1 = resp1.json()["data"]
        cat2 = resp2.json()["data"]

    # Act
    with allure.step("Попытка переименовать cat2 в имя cat1"):
        update_resp = requests.patch(f"{api_base_url}/{cat2['id']}", json={"name": name1})
    
    # Assert
    with allure.step("Проверяем успешное создание котов"):
        assert resp1.status_code == 201
        assert resp2.status_code == 201
    with allure.step("Проверяем ошибку при попытке обновления"):
        assert update_resp.status_code == 409


