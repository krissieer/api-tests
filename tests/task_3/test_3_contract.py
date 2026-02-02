import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload
import utils.openapi_validator

@pytest.mark.task3
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/summary")
def test_get_summary_contract(api, openapi_validator):
    # # Arrange
    # with allure.step("Создаём нового пользователя"):
    #     create_user_resp = api.create_user(generate_unique_user_payload())
    # patch_payload =  {"userId": create_user_resp.json()["id"]}

    # with allure.step("Создаём нового кота"):
    #     create_cat_resp = api.create_cat({"name": generate_unique_cat_name(), "age": 7, "breed": "GET/stats"})
    # cat_id = create_cat_resp.json()["id"]

    # with allure.step("Обновляем данные кота о владельце"):
    #     patch_resp = api.adopt_cat(cat_id, patch_payload)

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_summary_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stat_resp)

@pytest.mark.task3
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/breeds")
def test_get_stats_by_breeds_contract(api, openapi_validator):
    # # Arrange
    # with allure.step("Создаём нового кота"):
    #     create_cat_resp = api.create_cat({"name": generate_unique_cat_name(), "age": 7, "breed": "GET/stats"})
    # cat_id = create_cat_resp.json()["id"]

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_stats_by_breed()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stat_resp)

@pytest.mark.task3
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/top-adopters")
def test_stats_top_adopters_contract(api, openapi_validator):
    # # Arrange
    # with allure.step("Создаём нового пользователя"):
    #     create_user_resp = api.create_user(generate_unique_user_payload())
    # patch_payload =  {"userId": create_user_resp.json()["id"]}

    # with allure.step("Создаём нового кота"):
    #     create_cat_resp = api.create_cat({"name": generate_unique_cat_name(), "age": 7, "breed": "GET/stats"})
    # cat_id = create_cat_resp.json()["id"]

    # with allure.step("Обновляем данные кота о владельце"):
    #     patch_resp = api.adopt_cat(cat_id, patch_payload)
    
    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_adopters_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stat_resp)

