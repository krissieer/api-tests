import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/cats/{id} delete adopted cat")
def test_delete_adopted_cat_success(api):
    logger.info("[API] Clearing user's list of adopted cats after deleting a cat")

    # Arrange 
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём  кота"):
        logger.info(f"Создаём кота {payload_cat}")
        create_cat = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    with allure.step("Обновляем данные кошки о владельце"):
        logger.info("Обновляем данные кошки о владельце")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    # Act
    with allure.step("Фиксируем данные о кошках пользователя"):
        user_cat_before = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Данные о кошках пользователя: {user_cat_before}")
        allure.attach(str(user_cat_before), name="User's cats", attachment_type=allure.attachment_type.JSON)
   
    with allure.step("Удаляем кошку"):
        logger.info("Удаляем кошку")
        delete_user_resp = api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем наличие кошки у пользвоателя до удаления"):
        logger.info("Проверяем наличие кошки у пользвоателя до удаления")
        assert len(user_cat_before["cats"]) == 1, f"Ожидалось 1, получено {len(user_cat_before['cats'])}"
        assert user_cat_before["cats"][0]["id"] == cat_id, f"Ожидалось {cat_id}, получено {user_cat_before['cats'][1]['id']}"

    with allure.step("Проверяем, что кошка удалилась"):
        logger.info("Проверяем, что кошка удалилась")
        cat_after_delete = api.get_cat_by_id(cat_id)
        assert cat_after_delete.status_code == 404, f"Ожидалось 404, получено {cat_after_delete.status_code}"

    with allure.step("Проверяем наличие кошки у пользователя после удаления"):
        logger.info("Проверяем наличие кошки у пользвоателя после удаления")
        user_cat_after = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Данные о кошках пользователя: {user_cat_after}")
        allure.attach(str(user_cat_after), name="User's cats after deleting", attachment_type=allure.attachment_type.JSON)
        assert len(user_cat_after["cats"]) == 0, f"Ожидалось 0, получено {len(user_cat_after['cats'])}"