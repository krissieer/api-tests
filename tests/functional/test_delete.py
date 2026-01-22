import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Delete Cat")
def test_delete_cat_success(api_base_url):
    """Позитивный тест: удаление кота"""
    # Arrange 
    payload = {"name": generate_unique_cat_name(), "age": 1, "breed": "Ragdoll"}
    with allure.step("Создаём кота"):
        create_resp = requests.post(api_base_url, json=payload)
        #assert create_resp.status_code == 201
        cat_id = create_resp.json()["data"]["id"]

    # Act
    with allure.step("Удаляем кота"):
        delete_resp = requests.delete(f"{api_base_url}/{cat_id}")
        #assert delete_resp.status_code == 204

    # Assert
    with allure.step("Проверяем статус ответа"):
        assert create_resp.status_code == 201
        assert delete_resp.status_code == 204
    with allure.step("Проверяем, что объект удален"):
        get_resp = requests.get(f"{api_base_url}/{cat_id}")
        assert get_resp.status_code == 404

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Delete Cat")
def test_delete_nonexistent_cat(api_base_url):
    """Негативный тест: удаление несуществующего кота"""
    # Arrange
    invalid_id = 999999

    # Act
    with allure.step("Удаляем несуществующего кота"):
        response = requests.delete(f"{api_base_url}/invalid_id")

    # Assert 
    with allure.step("Проверяем код ошибки"):
        assert response.status_code == 400