# from jsonschema import validate, ValidationError
# from utils.schemas import CAT_SCHEMA, CREATE_CAT_DTO

# def assert_valid_schema(data, schema, name="schema"):
#     try:
#         validate(instance=data, schema=schema)
#     except ValidationError as e:
#         raise AssertionError(f"{name} violated: {e.message}")


# import json
# import os
# from jsonschema import validate, ValidationError

# # Загружаем контракт 
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# with open(os.path.join(BASE_DIR, "openapi.json"), "r", encoding="utf-8") as f:
#     CONTRACT = json.load(f)

# def assert_valid_schema(data, schema_name):
#     """
#     Берет схему прямо из компонентов контракта
#     schema_name: например, 'Cat' или 'CreateCatDto'
#     """
#     schema = CONTRACT["components"]["schemas"].get(schema_name)
#     if not schema:
#         raise ValueError(f"Схема {schema_name} не найдена в контракте!")
    
#     # Чтобы jsonschema понимала внутренние ссылки $ref, 
#     # в сложных контрактах используют RefResolver, 
#     # но для базовых схем достаточно передать саму схему и весь контракт для контекста
#     try:
#         validate(instance=data, schema=schema)
#     except ValidationError as e:
#         raise AssertionError(f"Контракт {schema_name} нарушен: {e.message}")