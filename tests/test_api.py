
from fastapi.testclient import TestClient
import pytest

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        main,
        "DOCUMENTS_FILE",
        tmp_path / "documents.json",
    )
    return TestClient(main.app)


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_document_creation(client):
    response = client.post(
        "/documents",
        json={
            "title": "Security Test",
            "content": "This is a test document.",
        },
    )

    assert response.status_code == 200
    assert response.json()["source_trust"] == "untrusted"
    assert response.json()["id"]


def test_empty_document_rejected(client):
    response = client.post(
        "/documents",
        json={
            "title": "",
            "content": "",
        },
    )

    assert response.status_code == 422


def test_document_search(client):
    client.post(
        "/documents",
        json={
            "title": "Authentication Policy",
            "content": "Multi-factor authentication is required.",
        },
    )

    response = client.post(
        "/search",
        json={"query": "authentication"},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["results"][0]["score"] == 1


def test_empty_search_rejected(client):
    response = client.post(
        "/search",
        json={"query": ""},
    )

    assert response.status_code == 422


def test_unmatched_search(client):
    response = client.post(
        "/search",
        json={"query": "nonexistentkeyword123"},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 0
