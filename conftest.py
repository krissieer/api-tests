import requests
import pytest
from utils.helpers import cleanup_test_cats

@pytest.fixture(autouse=True)
def clean_test_data(api_base_url):
    """Автоматически очищает тестовые данные до и после каждого теста"""
    cleanup_test_cats(api_base_url)
    yield
    cleanup_test_cats(api_base_url)

@pytest.fixture(scope="session")
def api_base_url():
    return "http://localhost:3000/cats"