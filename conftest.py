import pytest
import logging
from utils.helpers import cleanup_test_cats, cleanup_test_users
from utils.api_client import ShelterClient
from utils.openapi_validator import OpenAPIValidator
import uuid

@pytest.fixture(autouse=True)
def clean_test_data(api, auth_token):
    """Автоматически очищает тестовые данные котов до и после каждого теста"""
    cleanup_test_cats(api, auth_token)
    cleanup_test_users(api, auth_token)
    yield
    cleanup_test_cats(api, auth_token)
    cleanup_test_users(api, auth_token)

@pytest.fixture
def auth_token(api):
    payload = {
        "firstName": "Admin",
        "lastName": "Admin",
        "login": "admin",
        "password": "password123"
    }
    resp = api.login(payload)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return token

@pytest.fixture(scope="session")
def api():
    return ShelterClient(base_url="http://localhost:3000")

@pytest.fixture(scope="session")
def openapi_validator():
    return OpenAPIValidator("openapi.yaml")

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(levelname)s] [%(name)s] %(message)s"
    )

    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.INFO)