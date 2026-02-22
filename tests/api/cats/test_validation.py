import pytest
import allure
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
def test_invalid_cat_not_saved(api):
    logger.info("[API] Checking the immutability of the DB when trying to add invalid cat")
    
    # Arrange
    payload = {"name": "A", "age": -1, "breed": "API",}

    # Act
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="cats", attachment_type=allure.attachment_type.JSON)  
    
    with allure.step("Добавляем кота с невалидными данными"):
        logger.info(f"Добавляем кота с невалидными данными {payload}")
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Invalid payload", attachment_type=allure.attachment_type.JSON)          

    with allure.step("Получаем список после попытки добавления"):
        logger.info("Список после попытки добавления")
        after_resp = api.get_all_cats()
        logger.debug(f"Список котов: {after_resp.json()}")
        allure.attach(str(after_resp.json()), name="cats after trying addition", attachment_type=allure.attachment_type.JSON)  

    # Assert
    with allure.step("Сравниваем количество до и после попытки добавления"):
        initial_count = len(initial_resp.json())
        after_count = len(after_resp.json())
        logger.info(f"Количество до попытки добавления - {initial_count}, после - {after_count}")
        assert after_count == initial_count, f"Ожидалось {initial_count}, получено {after_count}"
