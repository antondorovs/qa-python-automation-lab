import pytest

from qa_python_lab.api_client import ApiClient


@pytest.mark.api
@pytest.mark.smoke
def test_get_existing_user(base_url: str) -> None:
    response = ApiClient(base_url).request("GET", "/api/users/1")
    assert response.status == 200
    assert response.body == {"id": 1, "name": "Anna Smith", "email": "anna@example.com"}


@pytest.mark.api
def test_missing_user_returns_404(base_url: str) -> None:
    response = ApiClient(base_url).request("GET", "/api/users/999")
    assert response.status == 404
    assert response.body == {"error": "User not found"}


@pytest.mark.api
@pytest.mark.contract
def test_list_user_contract(base_url: str) -> None:
    response = ApiClient(base_url).request("GET", "/api/users")
    assert response.status == 200
    assert len(response.body) == 2
    for user in response.body:
        assert set(user) == {"id", "name", "email"}
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str) and user["name"]
        assert isinstance(user["email"], str) and "@" in user["email"]


@pytest.mark.api
@pytest.mark.contract
def test_create_user_and_read_back(base_url: str) -> None:
    client = ApiClient(base_url)
    created = client.request("POST", "/api/users", {
        "name": " Carla ",
        "email": " CARLA@example.com ",
    })
    assert created.status == 201
    assert created.body == {"id": 3, "name": "Carla", "email": "carla@example.com"}
    assert client.request("GET", "/api/users/3").body == created.body


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"name": "Carla"}, id="missing-email"),
        pytest.param({"name": "  ", "email": "carla@example.com"}, id="blank-name"),
        pytest.param({"name": "Carla", "email": " \t "}, id="blank-email"),
        pytest.param({"name": "Carla", "email": 42}, id="non-string-email"),
    ],
)
def test_invalid_create_is_rejected(base_url: str, payload: dict[str, object]) -> None:
    client = ApiClient(base_url)
    response = client.request("POST", "/api/users", payload)
    assert response.status == 400
    assert response.body == {"error": "name and email are required"}
    assert len(client.request("GET", "/api/users").body) == 2


@pytest.mark.api
def test_create_user_with_existing_normalized_email_is_rejected(base_url: str) -> None:
    client = ApiClient(base_url)
    response = client.request("POST", "/api/users", {
        "name": "Another Anna",
        "email": " ANNA@example.com ",
    })
    assert response.status == 409
    assert response.body == {"error": "email already exists"}
    assert len(client.request("GET", "/api/users").body) == 2


@pytest.mark.api
def test_unknown_route_returns_404(base_url: str) -> None:
    response = ApiClient(base_url).request("GET", "/api/unknown")
    assert response.status == 404
