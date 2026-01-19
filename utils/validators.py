import allure

@allure.step("Проверка контракта объекта кота")
def assert_cat_contract(data):
    expected_fields = {"id", "name", "age", "breed"}
    assert set(data.keys()) == expected_fields, f"Ожидались поля: {expected_fields}, получены: {set(data.keys())}"
    assert isinstance(data["id"], int), "ID должен быть числом"
    assert isinstance(data["name"], str) and data["name"], "Имя должно быть непустой строкой"
    assert isinstance(data["age"], int), "Возраст должен быть числом"
    assert isinstance(data["breed"], str) and data["breed"], "Порода должна быть непустой строкой"