def assert_cat_response(data, expected_name, expected_age, expected_breed, expected_history=None, expected_description=None):
    assert "id" in data
    assert data["name"] == expected_name, f"Ожидалось {expected_name}, получено {data['name']}"
    assert data["age"] == expected_age, f"Ожидалось {expected_age}, получено {data['age']}"
    assert data["breed"] == expected_breed, f"Ожидалось {expected_breed}, получено {data['breed']}"
    assert data.get("history") == expected_history, f"Ожидалось {expected_history}, получено {data.get('history')}"
    assert data.get("description") == expected_description, f"Ожидалось {expected_description}, получено {data.get('description')}"

def assert_adoption_data(data, expected_status, expected_owner_id=None):
    assert "id" in data
    assert data["isAdopted"] is expected_status, f"Ожидалось {expected_status}, получено {data['isAdopted']}"
    owner = data.get("owner")
    if expected_owner_id is None:
        assert owner is None
    else:
        assert owner is not None
        assert owner["id"] == expected_owner_id, f"Ожидалось {expected_owner_id}, получено {owner['id']}"
    assert data["adoptionDate"] is not None, f"Oжидалась дата, получено {data['adoptionDate']}"

def assert_user_response(data, expected_login, expected_firstName, expected_lastName):
    assert "id" in data
    assert data["login"] == expected_login, f"Ожидалось {expected_login}, получено {data['login']}"
    assert data["firstName"] == expected_firstName, f"Ожидалось {expected_firstName}, получено {data['firstName']}"
    assert data["lastName"] == expected_lastName, f"Ожидалось {expected_lastName}, получено {data['lastName']}"
    