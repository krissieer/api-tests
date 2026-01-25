import pytest
import requests
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Get Cats")
def test_get_all_cats(api):
    """Позитивный тест: получение списка всех котов"""
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "Bengal"}

    with allure.step("Создаём временного кота"):
        create_resp = api.create_cat(payload)

    # Act
    with allure.step("Получаем список всех котов"):
        all_resp = api.get_all_cats()

    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert create_resp.status_code == 201
        cat_id = create_resp.json()["id"]

    with allure.step("Проверяем корректность списка котов"):
        assert all_resp.status_code == 200
        cats = all_resp.json()
        assert isinstance(cats, list)
        assert len(cats) >= 1
        assert any(cat["id"] == cat_id for cat in cats), \
            "Созданный кот не найден в списке"

@pytest.mark.functional
@allure.feature("Cats CRUD")
@allure.story("Get Cat by ID")
def test_get_cat_by_id_success(api):
    """Позитивный тест: получение кота по ID"""
    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 5, "breed": "Sphynx"}
    with allure.step("Создаём кота"):
        create_resp = api.create_cat(payload)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Запрашиваем кота по ID"):
        get_resp = api.get_cat_by_id(cat_id)
        
    # Assert 
    with allure.step("Проверяем корректность ответа"):
        assert create_resp.status_code == 201
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == cat_id


# INVALID_ID = [
#     (999999, "nonexistent id", 404),
#     ("abc", "invalid id format", 400)]
# @pytest.mark.functional
# @allure.feature("Cats CRUD")
# @allure.story("Get Cat by ID")
# @pytest.mark.parametrize("value, description, expected_status", INVALID_ID)
# def test_get_cat_by_invalid_id_format(api, value, description, expected_status):
#     """Негативный тест: запрос невалидного ID"""
#     # Act
#     with allure.step(f"Запрашиваем по некорректному ID: {description}"):
#         response = api.get_cat_by_id(value)

#     # Assert 
#     with allure.step("Проверяем код ошибки"):
#         assert response.status_code == expected_status