import pytest
import allure
from utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats")
def test_cat_list_length_changes(api):
    logger.info("[API] checking changing amount of cats")

    # Arrange
    payload = build_cat_payload()

    # Act
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial cat list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload}")        
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    with allure.step("Получаем список котов после добавления"):
        logger.info("Получаем список котов после добавления")
        after_create_resp = api.get_all_cats()
        logger.debug(f"Список котов: {after_create_resp.json()}")
        allure.attach(str(after_create_resp.json()), name="after addition cat list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Удаляем созданного кота"):
        logger.info("Удаляем созданного кота")
        delete_resp = api.delete_cat(cat_id)

    with allure.step("Получаем список котов после удаления"):
        logger.info("Получаем список котов после удаления")
        final_resp = api.get_all_cats()
        logger.debug(f"Список котов: {final_resp.json()}")
     
    # Assert
    with allure.step(f"Проверяем начальное количество котов: {len(initial_resp.json())}"):
        logger.info(f"Начальное количество котов: {len(initial_resp.json())}")
        initial_count = len(initial_resp.json())

    with allure.step("Проверяем, что после добавления количество котов увеличилось"):
        new_count = len(after_create_resp.json())
        logger.info(f"Количество котов после добавления: {new_count}")
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"

    with allure.step(f"Проверяем, что после удаления количество вернулось к исходному: {len(final_resp.json())}"):
        final_count = len(final_resp.json())
        logger.info(f"Количество котов после удаления: {final_count}")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"