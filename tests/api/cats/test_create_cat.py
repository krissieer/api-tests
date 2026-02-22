import pytest
import allure
from utils.data_builders import build_cat_payload, generate_unique_cat_name
from utils.models import assert_cat_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats")
def test_create_cat_and_get_by_id(api):
    logger.info("[API] Checking creaton and availability")

    # Arrange 
    payload = build_cat_payload()

    # Act
    with allure.step("Создаём кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload)
        cat_id = create_resp.json()["id"]

    with allure.step("Получаем созданного кота по его Id"):
        logger.info(f"Получаем созданного кота по его Id: {cat_id}")
        get_resp = api.get_cat_by_id(cat_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус создания: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"

    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp.json(), payload["name"], payload["age"], payload["breed"], payload.get("history"), payload.get("description"))


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats")
def test_multiple_cat_creation(api):
    logger.info("[API] Checking for multiple cat creation")    

    payloads = [
        build_cat_payload()
        for _ in range(3)
    ]
    created_ids = []

    # Act
    with allure.step("Создаём котов и добавляем их Id в список"):
        logger.info("Создаём котов и добавляем их Id в список")
        for payload in payloads:
            created_cat = api.create_cat(payload).json()
            logger.debug(f"Созданный кот: {created_cat}")
            created_ids.append(created_cat["id"])

    with allure.step("Получаем всех котов и их Id"):
        logger.info("Получаем всех котов и их Id")
        all_cats= api.get_all_cats().json()
        all_cat_ids = [cat["id"] for cat in all_cats]
        logger.debug(f"Список котов: {all_cats}")

    # Assert
    with allure.step("Сравниваем Id созданных и полученных из БД котов"):
        logger.info("Сравниваем Id созданных и полученных из БД котов")
        logger.debug(f"Список Id созданных котов: {created_ids}, Список Id из БД {all_cat_ids}")
        for cat_id in created_ids:
            assert cat_id in all_cat_ids