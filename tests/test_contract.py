import pytest
import requests
import allure
from utils.validators import assert_cat_contract
from utils.helpers import generate_unique_cat_name

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Response structure")
def test_cat_response_contract(api_base_url):
    name = generate_unique_cat_name()
    resp = requests.post(api_base_url, json={"name": name, "age": 3, "breed": "C"})
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert_cat_contract(data)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Response structure")
@pytest.mark.parametrize("invalid_payload", [
    {"age": 3, "breed": "B"},                                   # нет name
    {"name": "TestCat_", "breed": "B"},                         # нет age
    {"name": "TestCat_", "age": 3},                             # нет breed
    {"name": "TestCat_", "age": "not_a_number", "breed": "B"},  # строка вместо числа
    {"name": 5, "age": 5, "breed": 5},                          # число вместо строки
    {}])                                                        # пустой JSON
def test_cat_contract_invalid_input(api_base_url, invalid_payload):
    """Негативный тест: при отправке некорректных данных API не должен возвращать валидный объект кота."""
    with allure.step("Отправляем запрос с невалидными данными"):
        resp = requests.post(api_base_url, json=invalid_payload)

    with allure.step("Проверяем, что ответ не соответствует контракту"):
        assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
        response_json = resp.json()
        assert "data" not in response_json
        assert "message" in response_json or "error" in response_json
