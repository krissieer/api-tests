import pytest
import allure
from utils.data_builders import build_user_payload, build_cat_payload
from utils.models import assert_cat_response, assert_adoption_data
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id}")
def test_update_cat_success(api):
    logger.info("[API] Successful update cat's data with authorization")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat, token=token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    update_payload = build_cat_payload()

    # Act
    with allure.step("Обновляем данные"):
        logger.info(f"Обновление данных кота: {update_payload}")
        patch_resp = api.patch_cat(cat_id, update_payload, token=token)
        allure.attach(str(update_payload), name="New data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Получаем кота"):
        logger.info("Получаем данные кота")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Обновленные данные  кота: {cat}")
        allure.attach(str(cat), name="Cat after", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем обновленные данные"):
        logger.info("Проверяем обновленные данные")
        assert_cat_response(cat, update_payload["name"], update_payload["age"], \
        update_payload["breed"], update_payload.get("history"), update_payload.get("description"))


@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_success(api):
    logger.info("[API] Successful adoption with authorization")

    # Arrange 
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat, token=token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_cat.json()["id"]

    with allure.step("Получаем user_id из списка всех пользвоателей"):
        logger.info("Получаем user_id из списка всех пользвоателей")
        users = api.get_all_users(token=token).json()
        user_id = next(u["id"] for u in users if u["login"] == user_payload["login"])
    
    # Act
    with allure.step("Попытка обновления данных кота о новом владельце"):
        logger.info("Попытка обновления кота о новом владельце")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Assert
    with allure.step("Получаем кота"):
        logger.info("Получаем кота")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat}")
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем данные кота"):
        logger.info("Проверяем данные кота")
        assert_adoption_data(cat, True, user_id)

    with allure.step("Получаем данные о кошках пользователя"):
        logger.info("Получаем данные о кошках пользователя")
        user = api.get_adopted_cats_by_userId(user_id, token=token).json()
        logger.debug(f"Данные пользователя: {user}")
        allure.attach(str(user), name="Gotten user", attachment_type=allure.attachment_type.JSON)
        assert len(user["cats"]) == 1, f"Ожидалось 1, получено {len(user['cats'])}"
        assert user["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user['cats'][0]['id']}"

