import uuid
import requests

def generate_unique_cat_name(prefix="TestCat"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def cleanup_test_cats(api_base_url):
    """Удаляет всех котов, чьи имена начинаются с 'TestCat_'"""
    try:
        response = requests.get(api_base_url)
        if response.status_code == 200:
            cats = response.json()["data"]
            for cat in cats:
                if cat.get("name", "").startswith("TestCat_"):
                    requests.delete(f"{api_base_url}/{cat['id']}")
                    check = requests.get(f"{api_base_url}/{cat['id']}")
                    if check.status_code == 200:
                        print(f"⚠️ Кот {cat['id']} не удалился!")
    except Exception as e:
        print(f"Ошибка очистки: {e}")

def assert_cat_response(data, expected_name, expected_age, expected_breed):
    assert "id" in data
    assert data["name"] == expected_name
    assert data["age"] == expected_age
    assert data["breed"] == expected_breed