import pytest
import allure
from utils.helpers import generate_unique_cat_name, assert_cat_response

@pytest.mark.theonly
@pytest.mark.task2
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("PATCH/cats/{id}")
def test_update_cat_success(api):
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


    
