from fastapi.testclient import TestClient
from core.models import HighScore


def test_add_score(client: TestClient) -> None:
    # clear all scores to start
    response = client.post("/clear_scores")
    assert response.status_code == 200
    # add two scores to DB
    response = client.post("/add_score?initials=BCC&score=50000")
    assert response.status_code == 200
    high_score = response.json()
    assert high_score['initials'] == 'BCC'
    assert high_score['score'] == 50000
    response = client.post("/add_score?initials=DMC&score=60000")
    assert response.status_code == 200
    # query scores and make sure all IDs in each table row are non-null.
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
    for entry in content:
        assert entry['id'] is not None
    # clear high scores, then make sure they are actually cleared.
    response = client.post("/clear_scores")
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert content == []


def test_addscore_score_but_no_initials(client: TestClient) -> None:
    response = client.post('/add_score?initials=BCC')
    assert response.status_code == 422  # unprocessable content


def test_addscore_initials_but_no_score(client: TestClient) -> None:
    response = client.post('/add_score?score=120000')
    assert response.status_code == 422  # unprocessable content


def test_three_highscores_returns_sorted(client: TestClient) -> None:
    # start by clearing out existing high scores
    response = client.post('/clear_scores')
    assert response.status_code == 200

    # add one higher score
    response = client.post("/add_score?initials=BCC&score=50000")
    assert response.status_code == 200

    # add one lower score and make sure scores are sorted descending
    response = client.post('/add_score?initials=BCC&score=10000')
    assert response.status_code == 200

    response = client.post('/add_score?initials=DMC&score=11000')
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    expected = [
        HighScore(initials='AMC', score=12000),
        HighScore(initials='DMC', score=11000),
        HighScore(initials='BCC', score=10000)
    ]
    assert response == expected
