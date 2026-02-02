import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload

@pytest.mark.task3
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/stats/summary")
def test_stats_summary_counts_and_rate(api):
    """Проверка: общего числа кошек, числа усыновлённых, процента усыновления"""
    # Arrange
    with allure.step("Создаём 3ех котов"):
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 1, "breed": "Bengal"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 2, "breed": "Bengal"}).json()["id"]
        cat_3 = api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Sphynx"}).json()["id"]

    with allure.step("Создаём пользователя"):
        user_id = api.create_user(generate_unique_user_payload()).json()["id"]
        
    with allure.step("Обновляем данные 1го и 2го кота о владельце"):
        api.adopt_cat(cat_1, {"userId": user_id})
        api.adopt_cat(cat_2, {"userId": user_id})

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_summary_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200
    with allure.step("Проверяем общее количество котов"):
        assert stat_resp.json()["totalAnimals"] == 3
    with allure.step("Проверяем количество усыновленных котов"):
        assert stat_resp.json()["adoptedCount"] == 2
    with allure.step("Проверяем процент усыновленных котов"):
        rate_raw = stat_resp.json()["adoptionRate"]  
        rate = float(rate_raw.replace("%", ""))
        assert rate == pytest.approx(66.67, rel=0.1)
    
@pytest.mark.task3
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/stats/breeds")
def test_stats_breeds_grouping(api):
    """Группировка котов по породам"""
    # Arrange
    with allure.step("Создаём 3ех котов"):
        api.create_cat({"name": generate_unique_cat_name(), "age": 1, "breed": "Test_breed_1"})
        api.create_cat({"name": generate_unique_cat_name(), "age": 2, "breed": "Test_breed_1"})
        api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Test_breed_2"})

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_stats_by_breed()
    breeds = stat_resp.json()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200
    with allure.step("Проверяем количество котов каждой породы"):
        breeds_map = {b["breed"]: b["count"] for b in breeds}
        assert breeds_map["Test_breed_1"] == "2"
        assert breeds_map["Test_breed_2"] == "1"

@pytest.mark.task3
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/stats/top-adopters")
def test_stats_top_adopters(api):
    """Топ пользователей по числу усыновлений"""
    # Arrange
    with allure.step("Создаём пользователей"):
        user_1 = api.create_user(generate_unique_user_payload()).json()["id"]
        user_2 = api.create_user(generate_unique_user_payload()).json()["id"]
    
    with allure.step("Создаём 5 котов"):
        cats = [
            api.create_cat({"name": generate_unique_cat_name(), "age": i, "breed": "Mix"}).json()["id"]
            for i in range(1, 6)
        ]

    with allure.step("Обновляем данные 1, 2, 3, 4 кота о владельце"):
        api.adopt_cat(cats[0], {"userId": user_1})
        api.adopt_cat(cats[1], {"userId": user_1})
        api.adopt_cat(cats[2], {"userId": user_1})
        api.adopt_cat(cats[3], {"userId": user_2})

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_adopters_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200

    with allure.step("Проверяем данные в ответе"):
        assert len(stat_resp.json()) == 2
        assert stat_resp.json()[0]["id"] == user_1
        assert stat_resp.json()[0]["count"] == "3"
        assert stat_resp.json()[1]["id"] == user_2
        assert stat_resp.json()[1]["count"] == "1"

@pytest.mark.task3
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats?isKitten=true")
def test_filter_kittens_only(api):
    """Фильтр котят (< 1 года)"""
    # Arrange
    with allure.step("Создаём 2ух котов"):
        api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Siamese"})
        api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Siamese"})

    # Act
    with allure.step("Получаем только котят (возраст < 1)"):
        get_resp = api.get_all_cats({"isKitten": "true"})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200
    with allure.step("Проверяем данные в ответе"):    
        assert len(get_resp.json()) == 1
        assert get_resp.json()[0]["age"] == 0

@pytest.mark.task3
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats combined filters")
def test_combined_filters_with_kitten(api):
    """Комбинация breed + isAdopted + isKitten"""
    # Arrange
    with allure.step("Создаём 2ух котов"):
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Test_breed_1"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Test_breed_2"}).json()["id"]
    
    with allure.step("Создаём пользователя"):
        user_id = api.create_user(generate_unique_user_payload()).json()["id"]

    with allure.step("Обновляем данные 1го кота о владельце"):
        api.adopt_cat(cat_1, {"userId": user_id})

    # Act
    with allure.step("Получаем только котят + Test_breed_1 + с владельцем"):
        get_resp = api.get_all_cats({"breed": "Test_breed_1", "isAdopted": "true", "isKitten": "true"})
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200
    with allure.step("Проверяем данные в ответе"): 
        assert len(get_resp.json()) == 1
        assert get_resp.json()[0]["breed"] == "Test_breed_1"
        assert get_resp.json()[0]["isAdopted"] is True
        assert get_resp.json()[0]["age"] < 1

@pytest.mark.task3
@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats empty response")
def test_get_empty_response(api):
    """Запрос с фильтром возвращает пустой список"""
    # Arrange
    with allure.step("Создаём 2ух котов"):
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Test_breed_1"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Test_breed_2"}).json()["id"]
    
    with allure.step("Создаём пользователя"):
        user_id = api.create_user(generate_unique_user_payload()).json()["id"]

    with allure.step("Обновляем данные 1го кота о владельце"):
        api.adopt_cat(cat_1, {"userId": user_id})

    # Act
    with allure.step("Получаем только котят  с владельцем"):
        get_resp = api.get_all_cats({"isAdopted": "true", "isKitten": "true"})
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200
    with allure.step("Проверяем, что список пустой"): 
        assert len(get_resp.json()) == 0
