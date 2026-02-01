import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload 

@pytest.mark.task2
@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Adoption Workflow")
def test_complete_adoption_lifecycle(api):
    """
    E2E-тест: цикл усыновления
    1. Создаём пользователя
    2. Создаём кота
    3. Изменяем данные кота
    4. Усыновляем кота
    5. Проверяем данные пользователя и кота
    6. Пытаемся усыновить повторно
    7. Удаляем кота и пользователя
    """
    # Arrange 
    user_payload = generate_unique_user_payload()
    # Act
    with allure.step("Создаём нового пользователя"):
        create_user_resp = api.create_user(user_payload)
        user_id = create_user_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание пользователя"):
        assert create_user_resp.status_code == 201
    
    # Arrange 
    cat_payload = {"name": generate_unique_cat_name(), "age": 1, "breed": "E2E"}
    # Act
    with allure.step("Cоздаем кота"):
        create_cat_resp = api.create_cat(cat_payload)
        cat_id = create_cat_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert create_cat_resp.status_code == 201
    
    # Arrange
    updete_payload = {"age": 5, "breed": "Updated Breed", "history": "Updated history", "description": "Updated description"}
    # Act
    with allure.step("Обновляем данные кота"):
        update_resp = api.patch_cat(cat_id, updete_payload)
    # Assert
    with allure.step("Проверяем успешное обновление данных кота"):
        assert update_resp.status_code == 200
        assert update_resp.json()["age"] == 5
        assert update_resp.json()["breed"] == "Updated Breed"
        assert update_resp.json()["history"] == "Updated history"
        assert update_resp.json()["description"] == "Updated description"   

    # Arrange
    adopt_payload =  {"userId": user_id}
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        patch_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert 
    with allure.step("Проверяем успешное обновление данных кота"):
        assert patch_resp.status_code == 200
        assert patch_resp.json()["isAdopted"] is True
        assert patch_resp.json()["owner"]["id"] == user_id
        assert patch_resp.json()["adoptionDate"] is not None
    with allure.step("Проверяем успешное обновление данных пользователя"):
        user_cats_resp = api.get_adopted_cats_by_userId(user_id)
        assert user_cats_resp.json()["cats"][0]["id"] == cat_id

    # Act
    with allure.step("Попытка повторного усыновления"):
        second_adopt_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert
    with allure.step("Проверяем ошибки повтороного усыновления"):
        assert second_adopt_resp.status_code == 400

    # Act
    with allure.step("Удаляем кота"):
        delete_cat_resp = api.delete_cat(cat_id)
    with allure.step("Удаляем пользователя"):
        delete_user_resp = api.delete_user(user_id)
    # Assert
    with allure.step("Проверяем удаление кота"):
        assert delete_cat_resp.status_code == 204
        get_cat_resp = api.get_cat_by_id(cat_id)
        assert get_cat_resp.status_code == 404
    with allure.step("Проверяем удаление пользователя"):
        assert delete_user_resp.status_code == 204
        get_user_resp = api.get_user_by_id(user_id)
        assert get_user_resp.status_code == 404