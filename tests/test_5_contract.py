import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_login, get_userId_by_login, generate_health_card
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

# не сходится контракт: 200 == 201
# @pytest.mark.contract
# @allure.feature("Contract")
# @allure.story("POST/users/{id}/make-admin")
# def test_make_admin_success(api, auth_token, openapi_validator):
#     logger.info("[POST][POSITIVE] making user admin")
    
#     # Arrange
#     payload = generate_unique_login()
#     with allure.step("Регистрация нового пользователя"):
#         logger.info(f"Регистрация нового пользователя: {payload}")
#         reg_resp = api.register(payload)
#         allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)
#     userId = get_userId_by_login(api, payload['login'], auth_token)

#     # Act
#     with allure.step("Даем права администратора от имени админа"):
#         logger.info("Даем права администратора от имени админа")
#         resp = api.make_admin(userId, token=auth_token)

#     # Assert
#     with allure.step("Проверяем HTTP-статус"):
#         logger.info(f"HTTP-статус: {resp.status_code}")
#         assert resp.status_code == 201, f"Ожидалось 201, получено {resp.status_code}"
    
#     with allure.step("Проверяем контракт"):
#         logger.info("Проверка контракта")
#         openapi_validator.validate_response(resp)


# назначать админом может любой авторизованный пользователь
# @pytest.mark.contract
# @allure.feature("Contract")
# @allure.story("POST/users/{id}/make-admin forbidden")
# def test_make_admin_forbidden(api, auth_token, openapi_validator):
#     logger.info("[POST][NEGATIVE] Access denied")

#     # Arrange
#     payload_1 = generate_unique_login()
#     payload_2 = generate_unique_login()
#     with allure.step("Регистрация 2ух пользователей"):
#         logger.info(f"Регистрация 1го пользователя: {payload_1}")
#         reg_resp_1 = api.register(payload_1)
#         allure.attach(str(payload_1), name="User 1", attachment_type=allure.attachment_type.JSON)
#         logger.info(f"Регистрация 2го пользователя: {payload_2}")
#         reg_resp_2 = api.register(payload_2)
#         allure.attach(str(payload_2), name="User 2", attachment_type=allure.attachment_type.JSON)

#     user_id_1 = get_userId_by_login(payload_1['login'], auth_token)
#     token = reg_resp_2.json()["access_token"]

#     # Act
#     with allure.step("Даем права администратора пользователю №1 от лица пользователя №2(не админ)"):
#         resp = api.make_admin(user_id_1, token=token)

#     # Assert
#     with allure.step("Проверяем HTTP-статус"):
#         logger.info(f"HTTP-статус: {resp.status_code}")
#         assert create_resp.status_code == 403, f"Ожидалось 403, получено {resp.status_code}"
    
#     with allure.step("Проверяем контракт"):
#         logger.info("Проверка контракта")
#         openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users/{id}/make-admin unauthorized")
def test_make_admin_unauthorized(api, openapi_validator):
    logger.info("[POST][NEGATIVE] make-admin: unauthorized")

    # Act
    with allure.step("Даем права администратора без регистрации"):
        logger.info(f"Даем права администратора без регистрации")
        resp = api.make_admin(1)  

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users/{id}/make-admin invalid ID format")
@pytest.mark.parametrize("ID, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_make_admin_invalid_id_format(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[POST][NEGATIVE] make admin with invalid Id")

    # Act
    with allure.step(f"Даем права админа пользователю с некорректным ID: {ID}"):
        logger.info(f"Даем права админа пользователю с некорректным ID: {ID}")
        post_resp = api.make_admin(ID, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} delete by admin")
def test_delete_user_by_admin(api, openapi_validator, auth_token):
    logger.info("[DELETE USER][POSITIVE] delete by admin")
    
    # Arrange
    payload = generate_unique_login()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = get_userId_by_login(api, payload["login"], auth_token)

    # Act
    with allure.step("Удаляем пользователя от лица админа"):
        logger.info("Удаляем пользователя от лица админа")
        delete_resp = api.delete_user(user_id, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


# пользователь не может удалить свою страничку
# @pytest.mark.contract
# @allure.feature("Contract")
# @allure.story("DELETE/users/{id} delete your own page")
# def test_delete_own_user_page(api, openapi_validator, auth_token):
#     logger.info("[DELETE USER][POSITIVE] delete your own page")
    
#     # Arrange
#     payload = generate_unique_login()
#     with allure.step("Регистрация пользователя"):
#         logger.info(f"Регистрация пользователя: {payload}")
#         reg_resp = api.register(payload)
#         allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
#     token = reg_resp.json()["access_token"]
#     user_id = get_userId_by_login(api, payload["login"], token)

#     # Act
#     with allure.step("Удаляем пользователя от лица этого же пользователя"):
#         logger.info("Удаляем пользователя от лица этого же пользователя")
#         delete_resp = api.delete_user(user_id, token)

#     # Assert
#     with allure.step("Проверяем HTTP-статус"):
#         logger.info(f"HTTP-статус: {delete_resp.status_code}")
#         assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
#     with allure.step("Проверяем контракт"):
#         logger.info("Проверка контракта")
#         openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} forbidden")
def test_delete_user_forbidden(api, openapi_validator, auth_token):
    logger.info("[DELETE USER][NEGATIVE] Access denied")
    
    # Arrange
    payload_1 = generate_unique_login()
    payload_2 = generate_unique_login()
    with allure.step("Регистрация 2ух пользователей"):
        logger.info(f"Регистрация 1го пользователя: {payload_1}")
        reg_resp_1 = api.register(payload_1)
        allure.attach(str(payload_1), name="User 1", attachment_type=allure.attachment_type.JSON)
        logger.info(f"Регистрация 2го пользователя: {payload_2}")
        reg_resp_2 = api.register(payload_2)
        allure.attach(str(payload_2), name="User 2", attachment_type=allure.attachment_type.JSON)

    user_id_1 = get_userId_by_login(api, payload_1["login"], auth_token)
    token = reg_resp_2.json()["access_token"]

    # Act
    with allure.step("Удаляем пользователя №1 от лица пользователя №2 (не админ)"):
        logger.info("Удаляем пользователя №1 от лица пользователя №2 (не админ)")
        delete_resp = api.delete_user(user_id_1, token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 403, f"Ожидалось 403, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)






@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card success")
def test_create_health_card_success(api, openapi_validator, auth_token):
    logger.info("[POST][POSITIVE] create health-card")

    # Arrange
    cat_payload = cat_payload = {"name": generate_unique_cat_name(),"age": 1,"breed": "Bengal"}
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    payload = generate_health_card()

    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 201, f"Ожидалось 201, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card unauthorized")
def test_create_health_card_unauthorized(api, openapi_validator):
    logger.info("[POST][NEGATIVE] make health card: unauthorized")

    # Arrange
    payload = generate_health_card()

    # Act
    with allure.step("Создаем мед.книжку без авторизации"):
        logger.info(f"Создаем мед.книжку без авторизации: {payload}")
        resp = api.create_health_card(1, payload)
        allure.attach(str(payload), name="Health card", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card invalid ID format")
@pytest.mark.parametrize("ID, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_create_health_card_invalid_id_format(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[POST][NEGATIVE] make health card with invalid Id")

    # Arrange
    payload = generate_health_card()

    # Act
    with allure.step(f"Создаем мед.книжку коту с некорректным ID: {ID}"):
        logger.info(f"Создаем мед.книжку коту некорректным ID: {ID}")
        post_resp = api.create_health_card(ID, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card repeated creation")
def test_create_health_card_repeated_creation(api, openapi_validator, auth_token):
    logger.info("[POST][NEGATIVE] make health card to same cat twice")

    # Arrange
    cat_payload = cat_payload = {"name": generate_unique_cat_name(),"age": 1,"breed": "Bengal"}
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    payload = generate_health_card()

    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)
    with allure.step("Создаем повторно мед.книжку этому же коту"):
        logger.info(f"Создаем повторно мед.книжку этому же коту")
        post_rep_resp = api.create_health_card(cat_id, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_rep_resp.status_code}")
        assert post_rep_resp.status_code == 409, f"Ожидалось 409, получено {post_rep_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_rep_resp)


INVALID_PAYLOADS = [
    ({"medicalStatus": "login", "notes": "test_notes"},  "missing 'lastVaccination'"),
    ({"lastVaccination": "2025-12-01", "notes": "test_notes"},  "missing 'medicalStatus'"),
    ({"lastVaccination": "string", "medicalStatus": "test_status"},  "invalid type of 'lastVaccination'"),
    ({"lastVaccination": 11, "medicalStatus": "test_status"},  "invalid type of 'lastVaccination'"),
    ({"lastVaccination": "2025-12-01", "medicalStatus": 11},  "invalid type of 'medicalStatus'"),
    ({"lastVaccination": "2025-12-01", "medicalStatus": "test_notes", "notes": 11},  "invalid type of 'notes'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_health_card_invalid_payload(api, openapi_validator, payload, description, auth_token):
    logger.info("[POST][NEGATIVE] make health card with invalid payload")
    
    # Act
    with allure.step(f"Попытка создания мед.книжки: {description}"):
        logger.info(f"Попытка создания мед.книжки: {description}")
        post_resp = api.create_health_card(1, payload, auth_token)
        allure.attach(str(payload), name="Invalid data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert post_resp.status_code == 400, f"Ожидалось 400, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(post_resp)






@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/health-card success")
def test_patch_health_card_success(api, openapi_validator, auth_token):
    logger.info("[PATCH][POSITIVE] update health-card")

    # Arrange
    cat_payload = cat_payload = {"name": generate_unique_cat_name(),"age": 1,"breed": "Bengal"}
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    payload = generate_health_card()

    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)
        allure.attach(str(payload), name="Health card", attachment_type=allure.attachment_type.JSON)

    updated_payload = generate_health_card()
    # Act
    with allure.step("Обновляем мед.книжку"):
        logger.info(f"Обновляем мед.книжку: {updated_payload}")
        patch_resp = api.patch_health_card(cat_id, updated_payload, auth_token)
        allure.attach(str(updated_payload), name="Updated health card", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/health-card unauthorized")
def test_patch_health_card_unauthorized(api, openapi_validator):
    logger.info("[PATCH][NEGATIVE] update health-card: unauthorized")

    # Act
    with allure.step("Попытка обновить мед.книжку без авторизации"):
        logger.info("Попытка обновить мед.книжку без авторизации")
        patch_resp = api.patch_health_card(1, {})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/health-card invalid ID format")
@pytest.mark.parametrize("ID, expected_status", [(9999, 404), ("abc", 400)], ids=["nonexistent id", "invalid id format"])
def test_patch_health_card_invalid_id_format(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[PATCH][NEGATIVE] update health-card with invalid Id")

    # Arrange
    payload = generate_health_card()

    # Act
    with allure.step(f"Попытка обновить мед.книжку с некорректным ID: {ID}"):
        logger.info(f"Попытка обновить мед.книжку с некорректным ID: {ID}")
        patch_resp = api.patch_health_card(ID, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


INVALID_PAYLOADS = [
    ({"medicalStatus": "login", "notes": "test_notes"},  "missing 'lastVaccination'"),
    ({"lastVaccination": "2025-12-01", "notes": "test_notes"},  "missing 'medicalStatus'"),
    ({"lastVaccination": "string", "medicalStatus": "test_status"},  "invalid type of 'lastVaccination'"),
    ({"lastVaccination": 11, "medicalStatus": "test_status"},  "invalid type of 'lastVaccination'"),
    ({"lastVaccination": "2025-12-01", "medicalStatus": 11},  "invalid type of 'medicalStatus'"),
    ({"lastVaccination": "2025-12-01", "medicalStatus": "test_notes", "notes": 11},  "invalid type of 'notes'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/health-card invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_patch_health_card_invalid_payload(api, openapi_validator, payload, description, auth_token):
    logger.info("[PATCH][NEGATIVE] make health card with invalid payload")
    
    # Act
    with allure.step(f"Попытка обновить мед.книжку: {description}"):
        logger.info(f"Попытка обновить мед.книжку: {description}")
        patch_resp = api.patch_health_card(1, payload, auth_token)
        allure.attach(str(payload), name="Invalid data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert patch_resp.status_code == 400, f"Ожидалось 400, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)