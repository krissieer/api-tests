import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/summary")
def test_get_summary_contract(api, openapi_validator):
    logger.info("[GET SUMMARY STATS] get total number of cats, adopted cats, adoption rate")

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
        allure.attach(str(stat_resp.json()), name="Stats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stat_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/breeds")
def test_get_stats_by_breeds_contract(api, openapi_validator):
    logger.info("[GET BREED STATS] get number of cats by breed")

    # # Arrange
    # with allure.step("Создаём нового кота"):
    #     create_cat_resp = api.create_cat({"name": generate_unique_cat_name(), "age": 7, "breed": "GET/stats"})
    # cat_id = create_cat_resp.json()["id"]

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_stats_by_breed()
        allure.attach(str(stat_resp.json()), name="Stats breed", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stat_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/top-adopters")
def test_stats_top_adopters_contract(api, openapi_validator):
    logger.info("[GET ADOPTERS STATS] get users who adopted cats")
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
        allure.attach(str(stat_resp.json()), name="Adopters", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(stat_resp)

