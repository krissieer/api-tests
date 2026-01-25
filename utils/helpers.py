import uuid
import requests

def generate_unique_cat_name(prefix="TestCat"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def cleanup_test_cats(api_client):
    """Удаляет всех котов, чьи имена начинаются с 'TestCat_'"""
    try:
        response = api_client.get_all_cats()
        if response.status_code == 200:
            cats = response.json()
            for cat in cats:
                if cat.get("name", "").startswith("TestCat_"):
                    api_client.delete_cat(cat['id'])
                    check = api_client.get_cat_by_id(cat['id'])
                    if check.status_code == 200:
                        print(f" Кот {cat['id']} не удалился!")
    except Exception as e:
        print(f"Ошибка очистки: {e}")

def assert_cat_response(data, expected_name, expected_age, expected_breed):
    assert "id" in data
    assert data["name"] == expected_name
    assert data["age"] == expected_age
    assert data["breed"] == expected_breed