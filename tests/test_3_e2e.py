import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload 
import logging
logger = logging.getLogger(__name__)


@pytest.mark.e2e
@allure.feature("End-to-End")
def test_full_stats_and_filtering(api):
    logger.info("[End-to-End] Data reconciliation in three types of statistics and filtering")

    # Arrange
    with allure.step("Создаём 2ух пользователей"):
        user_1 = api.create_user(generate_unique_user_payload()).json()["id"]
        user_2 = api.create_user(generate_unique_user_payload()).json()["id"]
        allure.attach(str(api.get_all_users().json()), name="All users", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём 6 котов"):
        cats = [
            api.create_cat({"name": generate_unique_cat_name(), "age": i % 2, "breed": "Bengal" if i % 2 == 0 else "Sphynx"}).json()["id"]
            for i in range(0, 5)
        ]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1, 2, 3, 4, 5 кота о владельце"):
        api.adopt_cat(cats[0], {"userId": user_1})
        api.adopt_cat(cats[1], {"userId": user_1})
        api.adopt_cat(cats[2], {"userId": user_1})
        api.adopt_cat(cats[3], {"userId": user_2})
        api.adopt_cat(cats[4], {"userId": user_2})
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act 
    with allure.step("Сбор общей статистики"):
        summary = api.get_summary_stats().json()
        allure.attach(str(summary), name="Summary stats", attachment_type=allure.attachment_type.JSON)
    with allure.step("Сбор статистики по породам"):
        breeds = api.get_stats_by_breed().json()
        allure.attach(str(breeds), name="Breed stats", attachment_type=allure.attachment_type.JSON)
    with allure.step("Сбор топа усыновителей"):
        top_adopters = api.get_adopters_stats().json()
        allure.attach(str(top_adopters), name="Adopters stats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Получаем только котят"):
        get_resp = api.get_all_cats({"isKitten": "true"}).json()
        allure.attach(str(get_resp), name="Kittens", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверям общее число котов"):
        assert summary["totalAnimals"] == 5, f"Ожидалось 5, получено {summary['totalAnimals']}"

    with allure.step("Проверям число усыновленных"):
        adopted_from_summary = int(summary["adoptedCount"])
        adopted_from_top = sum(int(user["count"]) for user in top_adopters)
        assert adopted_from_summary == adopted_from_top, f"Ожидалось {adopted_from_top}, получено {adopted_from_summary}"

    with allure.step("Проверям данные владельцкв"):
        assert top_adopters[0]["id"] == user_1, f"Ожидалось {user_1}, получено {top_adopters[0]['id']}"
        assert int(top_adopters[0]["count"]) > int(top_adopters[1]["count"])

    with allure.step("Проверям породы"):
        breed_counts = {b["breed"]: int(b["count"]) for b in breeds}
        total = breed_counts["Bengal"] + breed_counts["Sphynx"]
        assert total == 5,  f"Ожидалось 5, получено {total}"

    with allure.step("Проверям получение отфильтрованнх данных"):
        assert len(get_resp) == 3, f"Ожидалось 3, получено {len(get_resp)}"
        assert all(c["age"] == 0 and c["breed"] == "Bengal" for c in get_resp)
