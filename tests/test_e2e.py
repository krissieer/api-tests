import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
from utils.models import assert_cat_response, assert_adoption_data
import logging
logger = logging.getLogger(__name__)

@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Adoption Workflow")
def test_complete_adoption_lifecycle(api):
    logger.info("[End-to-End] adoption lifecycle")
    """
    E2E-тест: цикл усыновления
    1. Создаём пользователя
    2. Создаём кота
    3. Изменяем данные кота
    4. Усыновляем кота
    5. Проверяем данные пользователя и кота
    6. Пытаемся усыновить повторно
    7. Удаляем кота и пользователя
    """
    # Arrange 
    user_payload = build_user_payload()
    # Act
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создаём нового пользователя: {user_payload}")
        create_user_resp = api.create_user(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        user_id = create_user_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание пользователя"):
        logger.info(f"Проверяем успешное создание пользователя: {create_user_resp.status_code}")
        assert create_user_resp.status_code == 201, f"Ожидалось 201, получено {create_user_resp.status_code}"
    
    # Arrange 
    cat_payload = build_cat_payload()
    # Act
    with allure.step("Cоздаем кота"):
        logger.info(f"Cоздаем кота: {cat_payload}")
        create_cat_resp = api.create_cat(cat_payload)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_cat_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        logger.info(f"Проверяем успешное создание кота: {create_cat_resp.status_code}")
        assert create_cat_resp.status_code == 201, f"Ожидалось 201, получено {create_cat_resp.status_code}"
    
    # Arrange
    update_payload = build_cat_payload(history="Updated history", description="Updated description")
    # Act
    with allure.step("Обновляем данные кота"):
        logger.info(f"Обновляем данные кота: {update_payload}")
        update_resp = api.patch_cat(cat_id, update_payload)
        allure.attach(str(update_payload), name="New cat's data", attachment_type=allure.attachment_type.JSON)
    # Assert
    with allure.step("Проверяем успешное обновление данных кота"):
        logger.info(f"Проверяем успешное обновление данных кота: {update_resp.status_code}")
        assert update_resp.status_code == 200, f"Ожидалось 200, получено {update_resp.status_code}"
        cat = api.get_cat_by_id(cat_id).json()
        assert_cat_response(cat, update_payload["name"], update_payload["age"], update_payload["breed"], \
        update_payload["history"], update_payload["description"])

    # Arrange
    adopt_payload =  {"userId": user_id}
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        logger.info(f"Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert 
    with allure.step("Проверяем успешное обновление данных кота"):
        logger.info(f"Проверяем успешное обновление данных кота: {patch_resp.status_code}")
        assert patch_resp.status_code == 200,  f"Ожидалось 200, получено {patch_resp.status_code}"
        assert_adoption_data(patch_resp.json(), True, user_id)
    with allure.step("Проверяем успешное обновление данных пользователя"):
        user_cats_resp = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Обновленные данные пользователя: {user_cats_resp}")
        assert user_cats_resp["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user_cats_resp['cats'][0]['id']}"

    # Act
    with allure.step("Попытка повторного усыновления"):
        logger.info("Попытка повторного усыновления")
        second_adopt_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert
    with allure.step("Проверяем ошибки повтороного усыновления"):
        logger.info(f"Проверяем ошибки повтороного усыновления:{second_adopt_resp.status_code}")
        assert second_adopt_resp.status_code == 400, f"Ожидалось 400, получено {second_adopt_resp.status_code}"

    # Act
    with allure.step("Удаляем кота"):
        logger.info("Удаляем кота")
        delete_cat_resp = api.delete_cat(cat_id)
    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_user_resp = api.delete_user(user_id)
    # Assert
    with allure.step("Проверяем удаление кота"):
        logger.info(f"Проверяем удаление кота: {delete_cat_resp.status_code}")
        assert delete_cat_resp.status_code == 204, f"Ожидалось 204, получено {delete_cat_resp.status_code}"
        get_cat_resp = api.get_cat_by_id(cat_id)
        assert get_cat_resp.status_code == 404, f"Ожидалось 404, получено {get_cat_resp.status_code}"
    with allure.step("Проверяем удаление пользователя"):
        logger.info(f"Проверяем удаление пользователя: {delete_user_resp.status_code}")
        assert delete_user_resp.status_code == 204, f"Ожидалось 204, получено {delete_user_resp.status_code}"
        get_user_resp = api.get_user_by_id(user_id)
        assert get_user_resp.status_code == 404,  f"Ожидалось 404, получено {get_user_resp.status_code}"