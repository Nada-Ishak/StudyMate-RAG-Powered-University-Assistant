from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_query_happy_path():
    response = client.post(
        "/query",
        json={
            "question": "What is linear regression?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert isinstance(data["answer"], str)
    assert isinstance(data["sources"], list)


def test_query_invalid_input():
    response = client.post(
        "/query",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422