import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload

@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}")
def test_update_cat_success(api):
    """Успешное обновление данных кошки после изменения"""
    # Arrange
    name = generate_unique_cat_name()
    create_payload = {"name": name, "age": 1, "breed": "Integration", "history": "Integration"}

    with allure.step("Создаём кота"):
        create_cat_resp = api.create_cat(create_payload)

    cat_id = create_cat_resp.json()["id"]

    update_payload = {
        "name": "TestCat_UpdatedName",
        "breed": "TestCat_UpdatedName",
        "history": "Updated history"}

    # Act
    with allure.step("Обновляем данные"):
        patch_resp = api.patch_cat(cat_id, update_payload)

    # Assert
    with allure.step("Получаем кота"):
        get_resp = api.get_cat_by_id(cat_id)
        cat = get_resp.json()

    with allure.step("Проверяем, что обновленные данные"):
        assert cat["name"] == "TestCat_UpdatedName"
        assert cat["breed"] == "TestCat_UpdatedName"
        assert cat["history"] == "Updated history"

@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id} Name conflict")
def test_update_cat_name_conflict(api):
    """Данные о кошке не изменяются после нуспешного обновления имени"""
    # Arrange 
    name = generate_unique_cat_name()
    first_cat = {"name": name, "age": 1, "breed": "Test"}
    second_cat = {"name": "TestCat_NameToChange", "age": 2, "breed": "Test"}

    with allure.step("Создаём 1го кота"):
        create_cat_1 = api.create_cat(first_cat)
    with allure.step("Создаём 2го кота"):
        create_cat_2 = api.create_cat(second_cat)
    cat_id = create_cat_2.json()["id"]

    update_payload = {"name": name }

    # Act
    with allure.step("Попытка обновления имени 2го кота на имя 1го кота"):
        patch_resp = api.patch_cat(cat_id, update_payload)

    # Assert
    with allure.step("Получаем кота"):
        get_resp = api.get_cat_by_id(cat_id)
        cat = get_resp.json()

    with allure.step("Проверяем, что данные не обновились"):
        assert cat["name"] == "TestCat_NameToChange"
        assert cat["age"] == 2
        assert cat["breed"] == "Test"

@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_success(api):
    """Успешное обновление данных кошки и пользователя после изменения"""
    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(payload_user)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём кота"):
        create_cat = api.create_cat(payload_cat)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    # Assert
    with allure.step("Получаем кота"):
        get_resp = api.get_cat_by_id(cat_id)

    with allure.step("Проверяем данные кошки"):
        assert get_resp.json()["isAdopted"] is True
        assert get_resp.json()["owner"]["id"] == user_id
        assert get_resp.json()["adoptionDate"] is not None

    with allure.step("Получаем данные пользователя с кошками"):
        user_resp = api.get_adopted_cats_by_userId(user_id)
        assert len(user_resp.json()["cats"]) == 1
        assert user_resp.json()["cats"][0]["id"] == cat_id

@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("DELETE/users/{id}")
def test_user_deletion_sets_cat_owner_to_null(api):
    """При удалении пользователя кошка остаётся в системе, но становится без владельца"""
    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(payload_user)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём кота"):
        create_cat = api.create_cat(payload_cat)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    with allure.step("Удаляем пользователя"):
        delete_user_resp = api.delete_user(user_id)

    # Assert
    with allure.step("Проверяем, что кошка осталась, но данные владельца удалены"):
        cat_after_delete = api.get_cat_by_id(cat_id)
        cat_data = cat_after_delete.json()
        assert cat_data["isAdopted"] is True  
        assert cat_data["owner"] is None      

@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats Filtering")
def test_cat_list_filtering_by_breed_and_adoption_status(api):
    """Фильтрация списка кошек по породе и статусу усыновления"""
    # Arrange
    breed1 = "Bengal"
    breed2 = "Sphynx"

    with allure.step("Создаём список из 4 кошек"):
        cats = []
        for i, (breed, adopted) in enumerate([(breed1, False), (breed1, True), (breed2, False), (breed2, True)]):
            name = generate_unique_cat_name()
            with allure.step("Создаём кота"):
                create_cat = api.create_cat({"name": name, "age": 2, "breed": breed})
            cat_id = create_cat.json()["id"]
            
            if adopted:
                payload = generate_unique_user_payload()
                with allure.step("Создаём временного пользователя"):
                    create_resp = api.create_user(payload)
                user_id = create_resp.json()["id"]
                
                adopt_payload =  {"userId": user_id}
                with allure.step("Обновляем данные о владельце кошки"):
                    patch_resp = api.adopt_cat(cat_id, adopt_payload)
           
            with allure.step("Добавляем кота в список"):
                cats.append(cat_id)
            
    # Act
    def get_filtered(breed=None, is_adopted=None):
        params = {}
        if breed: params["breed"] = breed
        if is_adopted is not None: params["isAdopted"] = str(is_adopted).lower()
        get_resp = api.get_all_cats(params)
        assert get_resp.status_code == 200
        return get_resp.json()

    with allure.step("Фильтр: только Bengal"):
        bengals = get_filtered(breed="Bengal")

    with allure.step("Фильтр: только неусыновлённые"):
        free_cats = get_filtered(is_adopted=False)

    with allure.step("Фильтр: Bengal + усыновлённые"):
        adopted_bengals = get_filtered(breed="Bengal", is_adopted=True)

    # Assert
    with allure.step("Проверяем количество Bengal кошек"):
        assert len(bengals) == 2
        assert all(c["breed"] == "Bengal" for c in bengals)

    with allure.step("Проверяем количество кошек без владельца"):
        assert len(free_cats) == 2
        assert all(not c["isAdopted"] for c in free_cats)

    with allure.step("Проверяем количество Bengal кошек с владельцем"):
        assert len(adopted_bengals) == 1
        assert adopted_bengals[0]["breed"] == "Bengal"
        assert adopted_bengals[0]["isAdopted"] is True

@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}/adopt Multuple cats")
def test_adopt_cat_success(api):
    """Успешное обновление данных пользователя после усыновления нескольких кошек"""
    # Arrange 
    payload_user = generate_unique_user_payload()
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(payload_user)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat_1 = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём 1го кота"):
        create_cat_1 = api.create_cat(payload_cat_1)
    cat_1_id = create_cat_1.json()["id"]

    payload_cat_2 = {"name": generate_unique_cat_name(), "age": 1, "breed": "Test"}
    with allure.step("Создаём 2го кота"):
        create_cat_2 = api.create_cat(payload_cat_2)
    cat_2_id = create_cat_2.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце 1ой кошки"):
        patch_1_resp = api.adopt_cat(cat_1_id, adopt_payload)
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        patch_2_resp = api.adopt_cat(cat_2_id, adopt_payload)

    # Assert
    with allure.step("Проверяем данные 1ой кошки"):
        get_resp_1 = api.get_cat_by_id(cat_1_id)
        assert get_resp_1.json()["isAdopted"] is True
        assert get_resp_1.json()["owner"]["id"] == user_id
        assert get_resp_1.json()["adoptionDate"] is not None
    
    with allure.step("Проверяем данные 2ой кошки"):
        get_resp_2 = api.get_cat_by_id(cat_2_id)
        assert get_resp_2.json()["isAdopted"] is True
        assert get_resp_2.json()["owner"]["id"] == user_id
        assert get_resp_2.json()["adoptionDate"] is not None

    with allure.step("Получаем данные пользователя с кошками"):
        user_resp = api.get_adopted_cats_by_userId(user_id)
        assert len(user_resp.json()["cats"]) == 2
        assert user_resp.json()["cats"][0]["id"] == cat_1_id
        assert user_resp.json()["cats"][1]["id"] == cat_2_id


@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("DELETE/cats/{id} delete adopted cat")
def test_adopt_cat_success(api):
    """При удалении кошки с владельцем список кошек у пользователя очищается"""
    # Arrange 
    with allure.step("Создаём пользователя"):
        create_user = api.create_user(generate_unique_user_payload())
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = {"name": generate_unique_cat_name(), "age": 3, "breed": "Test"}
    with allure.step("Создаём  кота"):
        create_cat = api.create_cat(payload_cat)
    cat_id = create_cat.json()["id"]

    with allure.step("Обновляем данные кошки о владельце"):
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    # Act
    with allure.step("Фиксируем данные о кошках пользователя"):
        user_cat_before = api.get_adopted_cats_by_userId(user_id)
   
    with allure.step("Удаляем кошку"):
        delete_user_resp = api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем наличие кошки у пользвоателя до удаления"):
        assert len(user_cat_before.json()["cats"]) == 1
        assert user_cat_before.json()["cats"][0]["id"] == cat_id

    with allure.step("Проверяем, что кошка удалилась"):
        cat_after_delete = api.get_cat_by_id(cat_id)
        assert cat_after_delete.status_code == 404

    with allure.step("Проверяем наличие кошки у пользвоателя после удаления"):
        user_cat_after = api.get_adopted_cats_by_userId(user_id)
        assert len(user_cat_after.json()["cats"]) == 0