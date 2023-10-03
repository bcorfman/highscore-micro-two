from fastapi.testclient import TestClient


def test_clear_scores(client: TestClient) -> None:
    response = client.post("/clear_scores")
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert content == []
