from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_document_and_search_flow():
    payload = {
        "title": "Python",
        "content": "Python is a programming language frequently used for APIs and machine learning.",
    }
    created = client.post("/documents", json=payload)
    assert created.status_code == 201

    result = client.get("/search", params={"q": "programming APIs"})
    assert result.status_code == 200
    assert len(result.json()) >= 1
