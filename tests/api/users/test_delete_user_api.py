import pytest
import allure
from utils.data_builders import build_user_payload
from utils.models import assert_user_is_admin
from utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id} delete by admin")
def test_check_delete_user_by_admin(api, auth_token):
    logger.info("[API] check deleting by admin")
    
    # Arrange
    with allure.step("Получаем исходный список пользователей"):
        logger.info("Получаем исходный список пользователей")
        initial_resp = api.get_all_users(token=auth_token)
        initial_count = len(initial_resp.json())
        logger.debug(f"Список пользователей: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial user list", attachment_type=allure.attachment_type.JSON)

    payload = build_user_payload()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = get_userId_by_login(api, payload["login"], auth_token)

    # Act
    with allure.step("Удаляем пользователя от лица админа"):
        logger.info("Удаляем пользователя от лица админа")
        delete_resp = api.delete_user(user_id, token=auth_token)

    with allure.step("Попытка получить пользователя по ID"):
        logger.info("Попытка получить пользователя по ID")
        get_deleted = api.get_user_by_id(user_id, token=auth_token)

    with allure.step("Получаем список пользователей после удаления"):
        logger.info("Получаем список пользователей после удаления")
        final_resp = api.get_all_users(token=auth_token)
        final_count = len(final_resp.json())
        logger.debug(f"Список пользователей: {final_resp.json()}")

    # Assert
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"

    with allure.step("Проверяем HTTP-статус получения после удаления"):
        logger.info(f"HTTP-статус получения после удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"

    with allure.step("Проверяем, что после удаления количество вернулось к исходному"):
        logger.info("Количество пользователей после удаления")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"