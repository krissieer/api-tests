import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats kittens")
def test_filter_kittens_only(api):
    logger.info("[API] checking filtering cats by age")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        api.create_cat(build_cat_payload(age=0))
        api.create_cat(build_cat_payload(age=3))
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят (возраст < 1)"):
        logger.info("Получаем только котят (возраст < 1)")
        get_resp = api.get_all_cats({"isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Kittens", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем данные в ответе"): 
        logger.info("Проверяем данные в ответе")   
        assert len(get_resp.json()) == 1, f"Ожидалось 1, получено {len(get_resp.json())}"
        assert get_resp.json()[0]["age"] == 0, f"Ожидалось 0, получено {get_resp.json()[0]['age']}"


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats combined filters")
def test_combined_filters_with_kitten(api):
    logger.info("[API] checking filtering cats by age, breed and adoption status")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_1")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2")).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)
    
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя: {payload_user}")
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id})
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


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats empty response")
def test_get_empty_response(api):
    logger.info("[API] checking filtering return empty list")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=3, breed="Test_breed_1")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2")).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)
    
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя: {payload_user}")
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id})
        allure.attach(str(api.get_cat_by_id(cat_1).json()), name="Cat_1", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят с владельцем"):
        logger.info("Получаем только котят с владельцем")
        get_resp = api.get_all_cats({"isAdopted": "true", "isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Adopted kittens", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем, что список пустой"): 
        logger.info("Проверяем, что список пустой")
        assert len(get_resp.json()) == 0, f"Ожидалось 0, получено {len(get_resp.json())}"