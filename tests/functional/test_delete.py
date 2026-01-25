import pytest
import allure
from utils.helpers import generate_unique_cat_name

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Delete Cat")
def test_delete_cat_success(api):
    """Позитивный тест: удаление кота"""
    # Arrange 
    payload = {"name": generate_unique_cat_name(), "age": 1, "breed": "Ragdoll"}
    with allure.step("Создаём кота"):
        create_resp = api.create_cat(payload)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Удаляем кота"):
        delete_resp = api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем статус ответа"):
        assert create_resp.status_code == 201
        assert delete_resp.status_code == 204
    with allure.step("Проверяем, что объект удален"):
        get_resp = api.get_cat_by_id(cat_id)
        assert get_resp.status_code == 404

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Delete Cat")
def test_delete_nonexistent_cat(api):
    """Негативный тест: удаление несуществующего кота"""
    # Arrange
    invalid_id = 999999

    # Act
    with allure.step("Удаляем несуществующего кота"):
        response = api.delete_cat(invalid_id)

    # Assert 
    with allure.step("Проверяем код ошибки"):
        assert response.status_code == 404

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Delete Cat")
def test_delete_cat_twice(api):
    # Arrange
    payload = {"name": generate_unique_cat_name(), "age": 1, "breed": "Ragdoll"}
    with allure.step("Создаём кота"):
        create_resp = api.create_cat(payload)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Удаляем кота"):
        delete_resp = api.delete_cat(cat_id)
    with allure.step("Удаляем повторно"):
        second_delete = api.delete_cat(cat_id)

    # Assert 
    with allure.step("Проверяем статус ответа"):
        assert create_resp.status_code == 201
        assert delete_resp.status_code == 204
        assert second_delete.status_code == 404
