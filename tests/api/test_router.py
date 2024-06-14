from fastapi.testclient import TestClient
from httpx import Response

from src.common.consts import DEFAULT_MAX_REQUESTS_PER_SECOND
from src.main import app

FIND_COUNTRY_URL = "/v1/find-country"
VALID_IP = "176.28.59.100"

client = TestClient(app, raise_server_exceptions=False)


def assert_error_response(response: Response) -> None:
    response_data = response.json()
    assert "error" in response_data


def test_missing_query_param():
    response = client.get(FIND_COUNTRY_URL)
    assert response.status_code == 422, response.text
    assert_error_response(response)


def test_wrong_query_param_name():
    response = client.get(f"{FIND_COUNTRY_URL}?ipp={VALID_IP}")
    assert response.status_code == 422, response.text
    assert_error_response(response)


def test_invalid_ip():
    response = client.get(f"{FIND_COUNTRY_URL}?ip=1.1")
    assert response.status_code == 400, response.text
    assert_error_response(response)


def test_rate_limit(mock_default_env_vars, clear_rate_limit):
    for i in range(DEFAULT_MAX_REQUESTS_PER_SECOND):
        response = client.get(f"{FIND_COUNTRY_URL}?ip={VALID_IP}")

        if i == DEFAULT_MAX_REQUESTS_PER_SECOND - 1:
            assert response.status_code == 429, response.text
            assert "X-Retry-After" in response.headers
            assert_error_response(response)
        else:
            assert response.status_code == 200, response.text


def test_happy_flow(mock_default_env_vars):
    response = client.get(f"{FIND_COUNTRY_URL}?ip={VALID_IP}")
    assert response.status_code == 200, response.text

    response_data = response.json()
    assert response_data == {"city": "Madrid", "country": "Spain"}
