from fastapi.testclient import TestClient


def test_add_score(client: TestClient) -> None:
    response = client.post("/add_score?initials=BCC&score=50000")
    assert response.status_code == 200
    high_score = response.json()
    assert high_score['initials'] == 'BCC'
    assert high_score['score'] == 50000
    response = client.post("/add_score?initials=DMC&score=60000")
    assert response.status_code == 200
    response = client.post("/clear_scores")
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert content == []


def test_clear_scores(client: TestClient) -> None:
    response = client.post("/clear_scores")
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert content == []
