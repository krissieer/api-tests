import pytest
import allure
from utils.data_builders import build_user_payload, build_cat_payload
from utils.models import assert_cat_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats")
def test_create_cat_and_get_success(api):
    logger.info("[API] Checking cat creaton and availability with authorization")

    # Arrange 
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    payload = build_cat_payload()

    # Act
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        initial_count = len(initial_resp.json())
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial cat list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload, token=token)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_resp.json()["id"]

    with allure.step("Получаем созданного кота по его Id"):
        logger.info(f"Получаем созданного кота по его Id: {cat_id}")
        get_resp = api.get_cat_by_id(cat_id)

    with allure.step("Получаем список котов после добавления"):
        logger.info("Получаем список котов после добавления")
        after_create_resp = api.get_all_cats()
        new_count = len(after_create_resp.json())
        logger.debug(f"Список котов: {after_create_resp.json()}")
        allure.attach(str(after_create_resp.json()), name="after addition cat list", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус создания: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"

    with allure.step("Проверяем, что после добавления количество котов увеличилось"):
        logger.info(f"Количество котов после добавления: {new_count}")
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"

    
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp.json(), payload["name"], payload["age"], payload["breed"], \
        payload.get("history"), payload.get("description"))