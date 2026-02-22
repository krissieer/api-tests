import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
import utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats Filtering")
def test_cat_list_filtering(api):
    logger.info("[API] Filtering cats by breed and adoption status")
    
    # Arrange
    with allure.step("Создаём 4 кота"):
        logger.info("Создаём 4 кота")
        cat_1 = api.create_cat(build_cat_payload(age=1, breed="Bengal")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=2, breed="Bengal")).json()["id"]
        cat_3 = api.create_cat(build_cat_payload(age=3, breed="Sphynx")).json()["id"]
        cat_4 = api.create_cat(build_cat_payload(age=4, breed="Sphynx")).json()["id"]
        logger.debug(f"Список котов: {api.get_all_cats().json()}")
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём 2ух пользователей"):
        logger.info("Создаём 2ух пользователей")
        user_1 = api.create_user(build_user_payload()).json()["id"]
        user_2 = api.create_user(build_user_payload()).json()["id"]
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