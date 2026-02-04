import pytest
from utils.helpers import cleanup_test_cats, cleanup_test_users
from utils.api_client import ShelterClient
from utils.openapi_validator import OpenAPIValidator
import uuid

@pytest.fixture(autouse=True)
def clean_test_data(api,auth_token):
    """Автоматически очищает тестовые данные котов до и после каждого теста"""
    cleanup_test_cats(api, auth_token)
    cleanup_test_users(api, auth_token)
    yield
    cleanup_test_cats(api, auth_token)
    cleanup_test_users(api, auth_token)

@pytest.fixture
def auth_token(api):
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "login": f"user_{uuid.uuid4().hex[:6]}",
        "password": "password123"
    }
    resp = api.register(payload)
    assert resp.status_code == 201
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def api():
    return ShelterClient(base_url="http://localhost:3000")

@pytest.fixture(scope="session")
def openapi_validator():
    return OpenAPIValidator("openapi.yaml")
