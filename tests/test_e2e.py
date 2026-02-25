import pytest
import allure
from utils.data_builders import build_cat_payload, build_health_card, build_user_payload
from utils.helpers import get_userId_by_login
from utils.models import assert_health_card, assert_user_is_admin, assert_cat_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.e2e
@allure.feature("E2E")
def test_health_card_lifecycle(api, auth_token):
    logger.info("[End-to-End] creation and updating health card")

    # Arrange
    cat_payload = build_cat_payload()
    # Act
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(cat_resp.json(), cat_payload["name"], cat_payload["age"], \
        cat_payload["breed"], cat_payload.get("history"), cat_payload.get("description"))

    # Arrange
    payload = build_health_card()
    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token).json()
    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_health_card(post_resp, payload["lastVaccination"], payload["medicalStatus"], payload.get("notes"))
        assert_cat_response(post_resp["cat"], cat_payload["name"], cat_payload["age"], cat_payload["breed"], \
        cat_payload.get("history"), cat_payload.get("description")) 

    # Arrange
    updated_payload = build_health_card()
    # Act
    with allure.step("Обновляем мед.книжку"):
        logger.info(f"Обновляем мед.книжку: {updated_payload}")
        patch_resp = api.patch_health_card(cat_id, updated_payload, auth_token)
        allure.attach(str(updated_payload), name="Updated health card", attachment_type=allure.attachment_type.JSON)
    with allure.step("Получаем созданного кота по Id"):
        logger.info("Получаем созданного кота по Id")
        get_resp = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Найденный кот: {get_resp}")
        allure.attach(str(get_resp), name="gotten cat", attachment_type=allure.attachment_type.JSON)
    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_health_card(patch_resp.json(), updated_payload["lastVaccination"], updated_payload["medicalStatus"], updated_payload.get("notes"))

    with allure.step("Проверяем данные кота после обновления мед.карты"):
        logger.info("Проверяем данные кота после обновления мед.карты")
        assert_health_card(get_resp["healthCard"], updated_payload["lastVaccination"], updated_payload["medicalStatus"], updated_payload.get("notes"))


@pytest.mark.e2e
@allure.feature("E2E")
@allure.story("delegated admin rights")
def test_new_admin_can_delete_other_users(api, auth_token):
    logger.info("[End-to-End] delegated admin can delete another user")

    # Arrange 
    user_1_payload = build_user_payload()
    user_2_payload = build_user_payload()

    # Act
    with allure.step("Регистрация 1го пользователя"):
        logger.info(f"Регистрация 1го пользователя: {user_1_payload}")
        reg_resp_1 = api.register(user_1_payload)
        allure.attach(str(user_1_payload), name="login data", attachment_type=allure.attachment_type.JSON)
    user_1 = get_userId_by_login(api, user_1_payload['login'], auth_token)

    with allure.step("Регистрация 2го пользователя"):
        logger.info(f"Регистрация 2го пользователя: {user_2_payload}")
        reg_resp_2 = api.register(user_2_payload)
        allure.attach(str(user_2_payload), name="login data", attachment_type=allure.attachment_type.JSON)
    user_2 = get_userId_by_login(api, user_2_payload['login'], auth_token)

    # Assert 
    with allure.step("Проверяем успешную регистрацию 1го пользователя"):
        logger.info(f"Проверяем успешную регистрацию 1го пользователя: {reg_resp_1.status_code}")
        assert reg_resp_1.status_code == 201, f"Ожидалось 201, получено {reg_resp_1.status_code}"
        assert "access_token" in reg_resp_1.json()
    with allure.step("Проверяем успешную регистрацию 2го пользователя"):
        logger.info(f"Проверяем успешную регистрацию 2го пользователя: {reg_resp_2.status_code}")
        assert reg_resp_2.status_code == 201, f"Ожидалось 201, получено {reg_resp_2.status_code}"
        assert "access_token" in reg_resp_2.json()

    # Act 
    with allure.step("Даем права администратора пользователю №1 от имени суперадмина"):
        logger.info("Даем права администратора пользователю №1 от имени суперадмина")
        admin_resp = api.make_admin(user_1, token=auth_token)
    
    # Assert 
    with allure.step("Проверяем передачу прав"):
        logger.info("Проверяем передачу прав")
        assert_user_is_admin(admin_resp.json(), user_1_payload["login"], user_1_payload["firstName"], user_1_payload["lastName"])
    
    # Arrange -
    with allure.step("Авторизация пользователя №1 - нового админа"):
        logger.info(f"Авторизация пользователя №1- нового админа")
        log_resp = api.login({"login": user_1_payload["login"], "password": user_1_payload["password"]})
        token = log_resp.json()["access_token"]
    
    # Act -
    with allure.step("Удаляем пользователя №2"):
        logger.info("Удаляем пользователя №2")
        delete_resp = api.delete_user(user_2, token=token)
    with allure.step("Попытка получить пользователя №2 по ID"):
        logger.info("Попытка получить пользователя №2 по ID")
        get_deleted = api.get_user_by_id(user_2, token=token)

    # Assert 
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем HTTP-статус получения после удаления"):
        logger.info(f"HTTP-статус получения после удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"


@pytest.mark.e2e
@allure.feature("E2E")
@allure.story("profile deletion access control")
def test_deleting_profile_control(api, auth_token):
    logger.info("[E2E] non-owner cannot delete profile, owner can delete his own")

    # Arrange
    user_1_payload = build_user_payload()
    user_2_payload = build_user_payload()

    # Act
    with allure.step("Регистрация 1го пользователя"):
        logger.info(f"Регистрация 1го пользователя: {user_1_payload}")
        reg_resp_1 = api.register(user_1_payload)
        allure.attach(str(user_1_payload), name="login data", attachment_type=allure.attachment_type.JSON)
    user_1 = get_userId_by_login(api, user_1_payload['login'], auth_token)
    token_1 = reg_resp_1.json()["access_token"]

    with allure.step("Регистрация 2го пользователя"):
        logger.info(f"Регистрация 2го пользователя: {user_2_payload}")
        reg_resp_2 = api.register(user_2_payload)
        allure.attach(str(user_2_payload), name="login data", attachment_type=allure.attachment_type.JSON)
    user_2 = get_userId_by_login(api, user_2_payload['login'], auth_token)
    token_2 = reg_resp_2.json()["access_token"]

    # Assert 
    with allure.step("Проверяем успешную регистрацию пользователей"):
        logger.info(f"Проверяем успешную регистрацию пользователей")
        assert reg_resp_1.status_code == 201, f"Ожидалось 201, получено {reg_resp_1.status_code}"
        assert "access_token" in reg_resp_1.json()
        assert reg_resp_2.status_code == 201, f"Ожидалось 201, получено {reg_resp_2.status_code}"
        assert "access_token" in reg_resp_2.json()

    # Act 
    with allure.step("Попытка удаления пользователя №2 от лица пользователя №1 (не админ)"):
        logger.info("Попытка удаления пользователя №2 от лица пользователя №1 (не админ)")
        try_delete_resp = api.delete_user(user_2, token_1)
    with allure.step("Получение пользователя №2 по ID"):
        logger.info("Получение пользователя №2 по ID")
        get_user_2 = api.get_user_by_id(user_2, token=auth_token)

    # Assert 
    with allure.step("Проверяем, что удаление не выполнено"):
        logger.info(f"Проверяем, что удаление не выполнено: {try_delete_resp.status_code}")
        assert try_delete_resp.status_code == 403, f"Ожидалось 403, получено {try_delete_resp.status_code}"
        assert get_user_2.status_code == 200, f"Ожидалось 200, получено {get_user_2.status_code}"

    # Act 
    with allure.step("Удаление пользователем №2 своей страницы"):
        logger.info("Удаление пользователем №2 своей страницы")
        delete_resp = api.delete_user(user_2, token_2)
    with allure.step("Получение пользователя №2 по ID"):
        logger.info("Получение пользователя №2 по ID")
        get_deleted_user = api.get_user_by_id(user_2, token=auth_token)

    # Assert 
    with allure.step("Проверяем, что удаление выполнено"):
        logger.info(f"Проверяем, что удаление выполнено: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
        assert get_deleted_user.status_code == 404, f"Ожидалось 404, получено {get_deleted_user.status_code}"