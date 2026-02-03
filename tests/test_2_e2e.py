import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload 
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
    user_payload = generate_unique_user_payload()
    # Act
    with allure.step("Создаём нового пользователя"):
        create_user_resp = api.create_user(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        user_id = create_user_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание пользователя"):
        assert create_user_resp.status_code == 201, f"Ожидалось 201, получено {create_user_resp.status_code}"
    
    # Arrange 
    cat_payload = {"name": generate_unique_cat_name(), "age": 1, "breed": "E2E"}
    # Act
    with allure.step("Cоздаем кота"):
        create_cat_resp = api.create_cat(cat_payload)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_cat_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert create_cat_resp.status_code == 201, f"Ожидалось 201, получено {create_cat_resp.status_code}"
    
    # Arrange
    updete_payload = {"age": 5, "breed": "Updated Breed", "history": "Updated history", "description": "Updated description"}
    # Act
    with allure.step("Обновляем данные кота"):
        update_resp = api.patch_cat(cat_id, updete_payload)
        allure.attach(str(updete_payload), name="New cat's data", attachment_type=allure.attachment_type.JSON)
    # Assert
    with allure.step("Проверяем успешное обновление данных кота"):
        assert update_resp.status_code == 200, f"Ожидалось 200, получено {update_resp.status_code}"
        cat = api.get_cat_by_id(cat_id).json()
        assert cat["age"] == updete_payload["age"], f"Ожидалось {updete_payload['age']}, получено {cat['age']}"
        assert cat["breed"] == updete_payload["breed"], f"Ожидалось {updete_payload['breed']}, получено {cat['breed']}"
        assert cat["history"] == updete_payload["history"], f"Ожидалось {updete_payload['history']}, получено {cat['history']}"
        assert cat["description"] == updete_payload["description"], f"Ожидалось {updete_payload['description']}, получено {cat['description']}"

    # Arrange
    adopt_payload =  {"userId": user_id}
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        patch_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert 
    with allure.step("Проверяем успешное обновление данных кота"):
        assert patch_resp.status_code == 200,  f"Ожидалось 200, получено {patch_resp.status_code}"
        assert patch_resp.json()["isAdopted"] is True, f"Ожидалось True, получено {patch_resp.json()['isAdopted']}"
        assert patch_resp.json()["owner"]["id"] == user_id, f"Ожидалось {user_id}, получено {patch_resp.json()['owner']['id']}"
        assert patch_resp.json()["adoptionDate"] is not None, f"Ожидалась дата, получено {patch_resp.json()['adoptionDate']}"
    with allure.step("Проверяем успешное обновление данных пользователя"):
        user_cats_resp = api.get_adopted_cats_by_userId(user_id).json()
        assert user_cats_resp["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user_cats_resp['cats'][0]['id']}"

    # Act
    with allure.step("Попытка повторного усыновления"):
        second_adopt_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert
    with allure.step("Проверяем ошибки повтороного усыновления"):
        assert second_adopt_resp.status_code == 400, f"Ожидалось 400, получено {second_adopt_resp.status_code}"

    # Act
    with allure.step("Удаляем кота"):
        delete_cat_resp = api.delete_cat(cat_id)
    with allure.step("Удаляем пользователя"):
        delete_user_resp = api.delete_user(user_id)
    # Assert
    with allure.step("Проверяем удаление кота"):
        assert delete_cat_resp.status_code == 204, f"Ожидалось 204, получено {delete_cat_resp.status_code}"
        get_cat_resp = api.get_cat_by_id(cat_id)
        assert get_cat_resp.status_code == 404, f"Ожидалось 404, получено {get_cat_resp.status_code}"
    with allure.step("Проверяем удаление пользователя"):
        assert delete_user_resp.status_code == 204, f"Ожидалось 204, получено {delete_user_resp.status_code}"
        get_user_resp = api.get_user_by_id(user_id)
        assert get_user_resp.status_code == 404,  f"Ожидалось 404, получено {get_user_resp.status_code}"