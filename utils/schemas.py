# CAT_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "id": {"type": "integer"},
#         "name": {"type": "string", "minLength": 2},
#         "age": {"type": "number", "minimum": 0},
#         "breed": {"type": "string"},
#         "history": {"type": ["string", "null"]},
#         "description": {"type": ["string", "null"]}
#     },
#     "required": ["id", "name", "age", "breed"]
# }

# CREATE_CAT_DTO = {
#     "type": "object",
#     "properties": {
#         "name": {"type": "string", "minLength": 2},
#         "age": {"type": "number", "minimum": 0},
#         "breed": {"type": "string"},
#         "history": {"type": ["string", "null"]},
#         "description": {"type": ["string", "null"]}
#     },
#     "required": ["name", "age", "breed"]
# }