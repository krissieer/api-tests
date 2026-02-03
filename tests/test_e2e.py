import pytest
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Full lifecycle of a cat")
def test_cat_full_lifecycle(api):
    logger.info("[End-to-End][POSITIVE] Cat's lifecycle")

    # Arrange 
    name = generate_unique_cat_name()
    payload = {"name": name, "age": 1, "breed": "E2E"}
    
    # Act
    with allure.step("Cоздаем кота"):
        create_resp = api.create_cat(payload)
        cat_id = create_resp.json()["id"]
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)

    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"

    # Act    
    with allure.step("Получаем список всех котов"):
        list_resp = api.get_all_cats()
        allure.attach(str(list_resp.json()), name="Cats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем получение списка"):
        assert list_resp.status_code == 200, f"Ожидалось 200, получено {list_resp.status_code}"
    with allure.step("Проверяем наличие созданного кота в списке"):
        cats = list_resp.json()
        assert any(c["id"] == cat_id for c in cats)
    
    # Act   
    with allure.step("Удаляем кота"):
        delete_resp = api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем удаление кота"):
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
        get_resp = api.get_cat_by_id(cat_id)
        assert get_resp.status_code == 404, f"Ожидалось 404, получено {deletget_respe_resp.status_code}"