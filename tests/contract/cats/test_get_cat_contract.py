import pytest
import allure
from utils.data_builders import build_cat_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_cat_by_Id_unauthorized_contract(api, openapi_validator, auth_token):
    logger.info("[GET CAT BY ID][POSITIVE] do not required to be authorized")
    
    # Arrange
    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Попытка получения кота по Id без регистрации"):
        logger.info(f"Попытка получения кота по Id: {cat_id}")
        get_resp = api.get_cat_by_id(cat_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_all_cats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET ALL CATS][POSITIVE] do not required to be authorized")
    
    # Act
    with allure.step("Попытка получения всех котов без регистрации"):
        logger.info("Попытка получения всех котов без регистрации")
        get_resp = api.get_all_cats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)