import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload 

@pytest.mark.task3
@pytest.mark.e2e
@allure.feature("End-to-End")
def test_full_stats_and_filtering(api):
    """Согласование данных в трех видах статистики и фильтрации"""
    # Arrange
    with allure.step("Создаём 2ух пользователей"):
        user_1 = api.create_user(generate_unique_user_payload()).json()["id"]
        user_2 = api.create_user(generate_unique_user_payload()).json()["id"]
    
    with allure.step("Создаём 6 котов"):
        cats = [
            api.create_cat({"name": generate_unique_cat_name(), "age": i % 2, "breed": "Bengal" if i % 2 == 0 else "Sphynx"}).json()["id"]
            for i in range(0, 5)
        ]

    with allure.step("Обновляем данные 1, 2, 3, 4, 5 кота о владельце"):
        api.adopt_cat(cats[0], {"userId": user_1})
        api.adopt_cat(cats[1], {"userId": user_1})
        api.adopt_cat(cats[2], {"userId": user_1})
        api.adopt_cat(cats[3], {"userId": user_2})
        api.adopt_cat(cats[4], {"userId": user_2})

    # Act 
    with allure.step("Сбор общей статистики"):
        summary = api.get_summary_stats().json()
    with allure.step("Сбор статистики по породам"):
        breeds = api.get_stats_by_breed().json()
    with allure.step("Сбор топа усыновителей"):
        top_adopters = api.get_adopters_stats().json()

    with allure.step("Получаем только котят"):
        get_resp = api.get_all_cats({"isKitten": "true"})

    # Assert
    with allure.step("Проверям общее число котов"):
        assert summary["totalAnimals"] == 5

    with allure.step("Проверям число усыновленных"):
        adopted_from_summary = int(summary["adoptedCount"])
        adopted_from_top = sum(int(user["count"]) for user in top_adopters)
        assert adopted_from_summary == adopted_from_top

    with allure.step("Проверям данные владельцкв"):
        assert top_adopters[0]["id"] == user_1
        assert int(top_adopters[0]["count"]) > int(top_adopters[1]["count"])

    with allure.step("Проверям породы"):
        breed_counts = {b["breed"]: int(b["count"]) for b in breeds}
        assert breed_counts["Bengal"] + breed_counts["Sphynx"] == 5

    with allure.step("Проверям получение отфильтрованнх данных"):
        assert len(get_resp.json()) == 3
        assert all(c["age"] == 0 and c["breed"] == "Bengal" for c in get_resp.json())
