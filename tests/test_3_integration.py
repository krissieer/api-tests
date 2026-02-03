import pytest
import allure
from utils.helpers import generate_unique_cat_name, generate_unique_user_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/stats/summary")
def test_stats_summary_counts_and_rate(api):
    logger.info("[Integration] checking total number of cats, adopted cats and adoption rate")

    # Arrange
    with allure.step("Создаём 3ех котов"):
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 1, "breed": "Bengal"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 2, "breed": "Bengal"}).json()["id"]
        cat_3 = api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Sphynx"}).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём пользователя"):
        payload_user = generate_unique_user_payload()
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
        
    with allure.step("Обновляем данные 1го и 2го кота о владельце"):
        api.adopt_cat(cat_1, {"userId": user_id})
        api.adopt_cat(cat_2, {"userId": user_id})

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_summary_stats()
        allure.attach(str(stat_resp.json()), name="Statistics", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем общее количество котов"):
        assert stat_resp.json()["totalAnimals"] == 3, f"Ожидалось 3, получено {stat_resp.json()['totalAnimals']}"
    with allure.step("Проверяем количество усыновленных котов"):
        assert stat_resp.json()["adoptedCount"] == 2, f"Ожидалось 2, получено {stat_resp.json()['adoptedCount']}"
    with allure.step("Проверяем процент усыновленных котов"):
        assert stat_resp.json()["adoptionRate"]  == pytest.approx(66.67, rel=0.1), f"Ожидалось 66.67, получено {stat_resp.json()['adoptionRate']}"
    

@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/stats/breeds")
def test_stats_breeds_grouping(api):
    logger.info("[Integration] checking stats by breed")

    # Arrange
    with allure.step("Создаём 3ех котов"):
        api.create_cat({"name": generate_unique_cat_name(), "age": 1, "breed": "Test_breed_1"})
        api.create_cat({"name": generate_unique_cat_name(), "age": 2, "breed": "Test_breed_1"})
        api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Test_breed_2"})
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_stats_by_breed()
        breeds = stat_resp.json()
        allure.attach(str(breeds), name="Breeds", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем количество котов каждой породы"):
        breeds_map = {b["breed"]: b["count"] for b in breeds}
        assert breeds_map["Test_breed_1"] == 2, f"Ожидалось 2, получено {breeds_map['Test_breed_1']}"
        assert breeds_map["Test_breed_2"] == 1, f"Ожидалось 1, получено {breeds_map['Test_breed_2']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/stats/top-adopters")
def test_stats_top_adopters(api):
    logger.info("[Integration] checking stats by top adopters")

    # Arrange
    with allure.step("Создаём пользователей"):
        user_1 = api.create_user(generate_unique_user_payload()).json()["id"]
        user_2 = api.create_user(generate_unique_user_payload()).json()["id"]
        allure.attach(str(api.get_all_users().json()), name="All users", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём 5 котов"):
        cats = [
            api.create_cat({"name": generate_unique_cat_name(), "age": i, "breed": "Mix"}).json()["id"]
            for i in range(1, 6)
        ]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1, 2, 3, 4 кота о владельце"):
        api.adopt_cat(cats[0], {"userId": user_1})
        api.adopt_cat(cats[1], {"userId": user_1})
        api.adopt_cat(cats[2], {"userId": user_1})
        api.adopt_cat(cats[3], {"userId": user_2})
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_adopters_stats()
        allure.attach(str(stat_resp.json()), name="Adopters", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"

    with allure.step("Проверяем данные в ответе"):
        assert len(stat_resp.json()) == 2, f"Ожидалось 2, получено {len(stat_resp.json())}"
        assert stat_resp.json()[0]["id"] == user_1, f"Ожидалось {user_1}, получено {stat_resp.json()[0]['id']}"
        assert stat_resp.json()[0]["count"] == 3, f"Ожидалось 3, получено {stat_resp.json()[0]['count']}"
        assert stat_resp.json()[1]["id"] == user_2, f"Ожидалось {user_2}, получено {stat_resp.json()[1]['id']}"
        assert stat_resp.json()[1]["count"] == 1, f"Ожидалось 1, получено {stat_resp.json()[1]['count']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats?isKitten=true")
def test_filter_kittens_only(api):
    logger.info("[Integration] checking filtering cats by age")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Siamese"})
        api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Siamese"})
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят (возраст < 1)"):
        get_resp = api.get_all_cats({"isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Kittens", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем данные в ответе"):    
        assert len(get_resp.json()) == 1, f"Ожидалось 1, получено {len(get_resp.json())}"
        assert get_resp.json()[0]["age"] == 0, f"Ожидалось 0, получено {get_resp.json()[0]['age']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats combined filters")
def test_combined_filters_with_kitten(api):
    logger.info("[Integration] checking filtering cats by age, breed and adoption status")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Test_breed_1"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Test_breed_2"}).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём пользователя"):
        payload_user = generate_unique_user_payload()
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        api.adopt_cat(cat_1, {"userId": user_id})
        allure.attach(str(api.get_cat_by_id(cat_1).json()), name="Cat_1", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят + Test_breed_1 + с владельцем"):
        get_resp = api.get_all_cats({"breed": "Test_breed_1", "isAdopted": "true", "isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Adopted Test_breed_1 kittens", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем данные в ответе"): 
        assert len(get_resp.json()) == 1, f"Ожидалось 1, получено {len(get_resp.json())}"
        assert get_resp.json()[0]["breed"] == "Test_breed_1", f"Ожидалось 'Test_breed_1', получено {get_resp.json()[0]['breed']}"
        assert get_resp.json()[0]["isAdopted"] is True, f"Ожидалось True, получено {get_resp.json()[0]['isAdopted']}"
        assert get_resp.json()[0]["age"] < 1, f"Ожидалось 0, получено {get_resp.json()[0]['age']}"


@pytest.mark.integration
@allure.feature("Integration")
@allure.story("GET/cats empty response")
def test_get_empty_response(api):
    logger.info("[Integration] checking filtering return empty list not error")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        cat_1 = api.create_cat({"name": generate_unique_cat_name(), "age": 3, "breed": "Test_breed_1"}).json()["id"]
        cat_2 = api.create_cat({"name": generate_unique_cat_name(), "age": 0, "breed": "Test_breed_2"}).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём пользователя"):
        payload_user = generate_unique_user_payload()
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        api.adopt_cat(cat_1, {"userId": user_id})
        allure.attach(str(api.get_cat_by_id(cat_1).json()), name="Cat_1", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят с владельцем"):
        get_resp = api.get_all_cats({"isAdopted": "true", "isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Adopted kittens", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем, что список пустой"): 
        assert len(get_resp.json()) == 0, f"Ожидалось 0, получено {len(get_resp.json())}"
