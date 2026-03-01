import pytest
import allure
from utils.data_builders import build_cat_payload, build_health_card, build_user_payload
from utils.models import assert_health_card, assert_cat_response, assert_adoption_data
from utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats/{id}")
def test_get_cat_with_health_card(api):
    logger.info("[API] get cat with health card")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    payload = build_health_card()
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, token)

    with allure.step("Обновление данных кота о новом владельце"):
        logger.info("Обновление данных кота о новом владельце")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Act
    with allure.step("Получаем созданного кота по Id"):
        logger.info("Получаем созданного кота по Id")
        get_resp = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Найденный кот: {get_resp}")
        allure.attach(str(get_resp), name="gotten cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp, cat_payload["name"], cat_payload["age"], cat_payload["breed"], cat_payload.get("history"), cat_payload.get("description"))
        assert_health_card(get_resp["healthCard"], payload["lastVaccination"], payload["medicalStatus"], payload.get("notes"))
        assert_adoption_data(get_resp, True, user_id)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats filters")
def test_get_cats_with_filters(api):
    logger.info("[API] checking filtering cats by age, breed and adoption status")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
    user_id = get_userId_by_login(api, user_payload['login'], token)

    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_1"), token=token).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2"), token=token).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id}, token=token)
        allure.attach(str(api.get_cat_by_id(cat_1).json()), name="Cat_1", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят + Test_breed_1 + с владельцем"):
        logger.info("Получаем только котят + Test_breed_1 + с владельцем")
        get_resp = api.get_all_cats({"breed": "Test_breed_1", "isAdopted": "true", "isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Adopted Test_breed_1 kittens", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем данные в ответе"): 
        logger.info("Проверяем данные в ответе")
        assert len(get_resp.json()) == 1, f"Ожидалось 1, получено {len(get_resp.json())}"
        assert get_resp.json()[0]["breed"] == "Test_breed_1", f"Ожидалось 'Test_breed_1', получено {get_resp.json()[0]['breed']}"
        assert get_resp.json()[0]["isAdopted"] is True, f"Ожидалось True, получено {get_resp.json()[0]['isAdopted']}"
        assert get_resp.json()[0]["age"] < 1, f"Ожидалось 0, получено {get_resp.json()[0]['age']}"


