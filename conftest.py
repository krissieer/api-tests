import requests
import pytest
import schemathesis
from utils.helpers import cleanup_test_cats
from utils.api_client import ShelterClient
from utils.openapi_validator import OpenAPIValidator

@pytest.fixture(autouse=True)
def clean_test_data(api):
    """Автоматически очищает тестовые данные до и после каждого теста"""
    cleanup_test_cats(api)
    yield
    cleanup_test_cats(api)

@pytest.fixture(scope="session")
def api():
    return ShelterClient(base_url="http://localhost:3000")


@pytest.fixture(scope="session")
def openapi_validator():
    return OpenAPIValidator("openapi.yaml")
