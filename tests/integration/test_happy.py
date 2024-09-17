import requests


def test_happy() -> None:
    url = "http://localhost:8000/api"

    try:
        response: requests.Response = requests.get(url, timeout=30)
    except requests.ConnectionError as exc:
        msg = "django server is not available"
        raise AssertionError(msg) from exc

    assert response.status_code == 200

    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "application/json"
