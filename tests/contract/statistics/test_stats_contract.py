import pytest
import allure
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_summary_unauthorized_contract(api, openapi_validator):
    logger.info("[GET SUMMARY][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики без регистрации"):
        logger.info("Попытка получения статистики без регистрации")
        stats_resp = api.get_summary_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stats_resp.status_code}")
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_breed_stats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET BREED STATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики без регистрации"):
        logger.info("Попытка получения статистики без регистрации")
        stats_resp = api.get_stats_by_breed()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stats_resp.status_code}")
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stats_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_adopters_stats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET ADOPTERS STATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики без регистрации"):
        logger.info("Попытка получения статистики без регистрации")
        stats_resp = api.get_adopters_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stats_resp.status_code}")
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stats_resp)