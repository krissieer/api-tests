import uuid

# Генерация имени для кошки
def generate_unique_cat_name():
    return f"TestCat_{uuid.uuid4().hex[:8]}"

# Генерация имени и фамилии для пользователя
def generate_unique_user_payload():
    name = f"TestUser_{uuid.uuid4().hex[:8]}"
    return {"firstName": name, "lastName": name}

# Генерация логина и пароля
def generate_unique_login():
    login = f"TestUser_{uuid.uuid4().hex[:8]}"
    password = f"password_{uuid.uuid4().hex[:8]}"
    user = generate_unique_user_payload()
    return {"firstName": user['firstName'], "lastName": user['lastName'], "login": login, "password": password}

# Удаление всех котов    
def cleanup_test_cats(api_client, auth_token):
    """Удаляет всех котов из БД"""
    try:
        response = api_client.get_all_cats()
        if response.status_code == 200:
            cats = response.json()
            for cat in cats:
                api_client.delete_cat(cat['id'], token=auth_token)
                check = api_client.get_cat_by_id(cat['id'])
                if check.status_code == 200:
                    print(f" Кот {cat['id']} не удалился!")
    except Exception as e:
        print(f"Ошибка очистки: {e}")

# Удаление пользователей
def cleanup_test_users(api_client, auth_token):
    """Удаляет всех пользователей из БД"""
    try:
        response = api_client.get_all_users(token=auth_token)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                api_client.delete_user(user['id'], token=auth_token)
                check = api_client.get_user_by_id(user['id'], token=auth_token)
                if check.status_code == 200:
                    print(f" Пользователь {user['id']} не удалился!")
                    
    except Exception as e:
        print(f"Ошибка очистки: {e}")

def assert_cat_response(data, expected_name, expected_age, expected_breed):
    assert "id" in data
    assert data["name"] == expected_name, f"Ожидалось {expected_name}, получено {data['name']}"
    assert data["age"] == expected_age, f"Ожидалось {expected_age}, получено {data['age']}"
    assert data["breed"] == expected_breed, f"Ожидалось {expected_breed}, получено {data['breed']}"