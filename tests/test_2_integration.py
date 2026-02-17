import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload
import logging
logger = logging.getLogger(__name__)

@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}")
def test_update_cat_success(api):
    logger.info("[Integration] Successful update cat's data after cat's data PATCH")
    
    # Arrange
    create_payload = {"name": generate_unique_cat_name(), "age": 1, "breed": "Integration", "history": "Integration"}

    with allure.step("Создаём кота"):
        logger.info(f"Создание нового кота: {create_payload}")
        create_cat_resp = api.create_cat(create_payload)
        allure.attach(str(create_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    update_payload = {
        "name": "TestCat_UpdatedName",
        "breed": "TestCat_UpdatedName",
        "history": "Updated history"}

    # Act
    with allure.step("Обновляем данные"):
        logger.info("Обновление данных кота")
        patch_resp = api.patch_cat(cat_id, update_payload)
        logger.debug(f"Новые данные: {update_payload}")
        allure.attach(str(update_payload), name="New data", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    # Assert
    with allure.step("Получаем кота"):
        logger.info("Получаем данные кота")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Обновленные данные  кота: {cat}")
        allure.attach(str(cat), name="Cat after", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем обновленные данные"):
        logger.info("Проверяем обновленные данные")
        assert cat["name"] == update_payload["name"], f"Ожидалось {update_payload['name']}, получено {cat['name']}"
        assert cat["breed"] == update_payload["breed"], f"Ожидалось {update_payload['breed']}, получено {cat['breed']}"
        assert cat["history"] == update_payload["history"], f"Ожидалось {update_payload['history']}, получено {cat['history']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id} Name conflict")
def test_update_cat_name_conflict(api):
    logger.info("[Integration] data doesn't change after unsuccessful PATCH")

    # Arrange 
    name = generate_unique_cat_name()
    first_cat = {"name": name, "age": 1, "breed": "Test"}
    second_cat = {"name": "TestCat_NameToChange", "age": 2, "breed": "Test"}

    with allure.step("Создаём 1го кота"):
        logger.info(f"Создание 1го кота: {first_cat}")
        create_cat_1 = api.create_cat(first_cat)
        allure.attach(str(first_cat), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создание 2го кота: {second_cat}")
        create_cat_2 = api.create_cat(second_cat)
        allure.attach(str(second_cat), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_2.json()["id"]

    update_payload = {"name": name }

    # Act
    with allure.step("Попытка обновления имени 2го кота на имя 1го кота"):
        logger.info("Попытка обновления имени 2го кота на имя 1го кота")
        patch_resp = api.patch_cat(cat_id, update_payload)

    # Assert
    with allure.step("Получаем кота после попытки обновления"):
        logger.info("Получаем кота после попытки обновления")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat}")
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем, что данные не обновились"):
        logger.info("Проверяем, что данные не обновились")
        assert cat["name"] == second_cat["name"], f"Ожидалось {second_cat['name']}, получено {cat['name']}"
        assert cat["age"] == second_cat["age"], f"Ожидалось {second_cat['age']}, получено {cat['age']}"
        assert cat["breed"] == second_cat["breed"], f"Ожидалось {second_cat['breed']}, получено {cat['breed']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_success(api):
    logger.info("[Integration] Successful update cat's and user's data after adoption")

    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    # Assert
    with allure.step("Получаем кота"):
        logger.info("Получаем кота")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat}")
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем данные кота"):
        logger.info("Проверяем данные кота")
        assert cat["isAdopted"] is True, f"isAdopted ожидалось True, получено {cat['isAdopted']}"
        assert cat["owner"]["id"] == user_id, f"Oжидалось {user_id}, получено {cat['owner']['id']}"
        assert cat["adoptionDate"] is not None, f"Oжидалась дата, получено {cat['adoptionDate']}"

    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user = api.get_adopted_cats_by_userId(user_id).json()

        logger.debug(f"Данные пользователя: {user}")
        allure.attach(str(user), name="Gotten user", attachment_type=allure.attachment_type.JSON)

        assert len(user["cats"]) == 1, f"Ожидалось 1, получено {len(user['cats'])}"
        assert user["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user['cats'][0]['id']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("DELETE/users/{id}")
def test_user_deletion_sets_cat_owner_to_null(api):
    logger.info("[Integration] Set NULL to cat's owner when user is deleted")

    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_user_resp = api.delete_user(user_id)

    # Assert
    with allure.step("Проверяем, что кошка осталась, но данные владельца удалены"):
        logger.info("Проверяем, что кошка осталась, но данные владельца удалены")
        cat_data = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat_data}")
        assert cat_data["isAdopted"] is True , f"Ожидалось True, получено {cat_data['isAdopted']}"
        assert cat_data["owner"] is None, f"Ожидалось Null, получено {cat_data['owner']}"

        get_resp = api.get_user_by_id(user_id)
        logger.debug(f"HTTP-статус получения пользователя: {get_resp.status_code}")
        assert get_resp.status_code == 404, f"Ожидалось 404, получено {get_resp.status_code}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats Filtering")
def test_cat_list_filtering_by_breed_and_adoption_status(api):
    logger.info("[Integration] Filtering cats by breed and adoption status")
    
    # Arrange
    with allure.step("Создаём 4 кота"):
        logger.info("Создаём 4 кота")
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 1, "breed": "Bengal"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 2, "breed": "Bengal"}).json()["id"]
        cat_3 = api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Sphynx"}).json()["id"]
        cat_4 = api.create_cat({"name": generate_unique_cat_name(), "age": 4, "breed": "Sphynx"}).json()["id"]
        logger.debug(f"Список котов: {api.get_all_cats().json()}")
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём 2ух пользователей"):
        logger.info("Создаём 2ух пользователей")
        create_1_user = api.create_user(generate_unique_user_payload())
        user_1 = create_1_user.json()["id"]
        create_2_user = api.create_user(generate_unique_user_payload())
        user_2 = create_2_user.json()["id"]
        logger.debug(f"Список пользователей: {api.get_all_users().json()}")
        allure.attach(str(api.get_all_users().json()), name="All users", attachment_type=allure.attachment_type.JSON)

    adopt_payload_1 = {"userId": user_1}
    adopt_payload_2 = {"userId": user_2}
    
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_resp_1 = api.adopt_cat(cat_2, adopt_payload_1)
    with allure.step("Обновляем данные о владельце 4ой кошки"):
        logger.info("Обновляем данные о владельце 4ой кошки")
        patch_resp_2 = api.adopt_cat(cat_4, adopt_payload_2)
  
    # Act
    with allure.step("Фильтр: только Bengal"):
        logger.info("Фильтр: только Bengal")
        bengals = api.get_all_cats({"breed":"Bengal"}).json()
        logger.debug(f"Список bengals котов: {bengals}")
        allure.attach(str(bengals), name="All bengals", attachment_type=allure.attachment_type.JSON)

    with allure.step("Фильтр: только неусыновлённые"):
        logger.info("Фильтр: только неусыновлённые")
        free_cats = api.get_all_cats({"isAdopted": "false"}).json()
        allure.attach(str(free_cats), name="All free cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Фильтр: Bengal + усыновлённые"):
        logger.info("Фильтр: только Bengal + усыновлённые")
        adopted_bengals = api.get_all_cats({"breed": "Bengal", "isAdopted": "true"}).json()
        logger.debug(f"Список Bengal + усыновлённые коты: {adopted_bengals}")
        allure.attach(str(adopted_bengals), name="All adopted bengals", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем количество Bengal кошек"):
        logger.info(f"Проверяем количество Bengal кошек: {len(bengals)}")
        assert len(bengals) == 2, f"Ожидалось 2, получено {len(bengals)}"
        assert all(c["breed"] == "Bengal" for c in bengals)

    with allure.step("Проверяем количество кошек без владельца"):
        logger.info(f"Проверяем количество кошек без владельца: {len(free_cats)}")
        assert len(free_cats) == 2, f"Ожидалось 2, получено {len(free_cats)}"
        assert all(not c["isAdopted"] for c in free_cats)

    with allure.step("Проверяем количество Bengal кошек с владельцем"):
        logger.info(f"Проверяем количество Bengal кошек с владельцем: {len(adopted_bengals)}")
        assert len(adopted_bengals) == 1, f"Ожидалось 1, получено {len(adopted_bengals)}"
        assert adopted_bengals[0]["breed"] == "Bengal", f"Ожидалось 'Bengal', получено {adopted_bengals[0]['breed']}"
        assert adopted_bengals[0]["isAdopted"] is True, f"Ожидалось True, получено {adopted_bengals[0]['isAdopted']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}/adopt Multuple cats")
def test_adopt_multiple_cats_success(api):
    logger.info("[Integration] Successful update user's data after multuple adoption")

    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat_1 = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём 1го кота"):
        logger.info(f"Создаём 1го кота {payload_cat_1}")
        create_cat_1 = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    cat_1_id = create_cat_1.json()["id"]

    payload_cat_2 = {"name": generate_unique_cat_name(), "age": 1, "breed": "Test"}
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создаём 2го кота {payload_cat_2}")
        create_cat_2 = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_2_id = create_cat_2.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце 1ой кошки"):
        logger.info("Обновляем данные о владельце 1ой кошки")
        patch_1_resp = api.adopt_cat(cat_1_id, adopt_payload)
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_2_resp = api.adopt_cat(cat_2_id, adopt_payload)

    # Assert
    with allure.step("Проверяем данные 1ой кошки"):
        logger.info("Проверяем данные 1ой кошки")
        get_resp_1 = api.get_cat_by_id(cat_1_id).json()
        logger.debug(f"Данные 1ой кошки: {get_resp_1}")
        allure.attach(str(get_resp_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
        assert get_resp_1["isAdopted"] is True, f"Ожидалось True, получено {get_resp_1['isAdopted']}"
        assert get_resp_1["owner"]["id"] == user_id, f"Ожидалось {user_id}, получено {get_resp_1['owner']['id']}"
        assert get_resp_1["adoptionDate"] is not None, f"Ожидалась дата, получено {get_resp_1['adoptionDate']}"
    
    with allure.step("Проверяем данные 2ой кошки"):
        logger.info("Проверяем данные 2ой кошки")
        get_resp_2 = api.get_cat_by_id(cat_2_id).json()
        logger.debug(f"Данные 1ой кошки: {get_resp_2}")
        allure.attach(str(get_resp_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
        assert get_resp_2["isAdopted"] is True, f"Ожидалось True, получено {get_resp_2['isAdopted']}"
        assert get_resp_2["owner"]["id"] == user_id, f"Ожидалось {user_id}, получено {get_resp_2['owner']['id']}"
        assert get_resp_2["adoptionDate"] is not None, f"Ожидалась дата, получено {get_resp_2['adoptionDate']}"

    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user_resp = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Данные пользователя: {user_resp}")
        allure.attach(str(user_resp), name="User", attachment_type=allure.attachment_type.JSON)
        assert len(user_resp["cats"]) == 2, f"Ожидалось 2, получено {len(user_resp['cats'])}"
        assert user_resp["cats"][0]["id"] == cat_1_id, f"Ожидалось {cat_1_id}, получено {user_resp['cats'][0]['id']}"
        assert user_resp["cats"][1]["id"] == cat_2_id, f"Ожидалось {cat_2_id}, получено {user_resp['cats'][1]['id']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("DELETE/cats/{id} delete adopted cat")
def test_delete_adopted_cat_success(api):
    logger.info("[Integration] Clearing user's list of adopted cats after deleting a cat")

    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
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