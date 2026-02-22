
def assert_cat_response(data, expected_name, expected_age, expected_breed):
    assert "id" in data
    assert data["name"] == expected_name, f"Ожидалось {expected_name}, получено {data['name']}"
    assert data["age"] == expected_age, f"Ожидалось {expected_age}, получено {data['age']}"
    assert data["breed"] == expected_breed, f"Ожидалось {expected_breed}, получено {data['breed']}"