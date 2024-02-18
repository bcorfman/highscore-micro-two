from fastapi.testclient import TestClient


def test_clear_scores(client: TestClient) -> None:
    response = client.post("/clear_scores")
    assert response.status_code == 200


def test_add_score(client: TestClient) -> None:
    # clear all scores to start
    response = client.post("/clear_scores")
    assert response.status_code == 200
    # add two scores to DB
    response = client.post("/add_score?initials=BCC&score=50000")
    assert response.status_code == 200
    high_score = response.json()
    assert high_score["initials"] == "BCC"
    assert high_score["score"] == 50000
    response = client.post("/add_score?initials=DMC&score=60000")
    assert response.status_code == 200
    high_score = response.json()
    assert high_score["initials"] == "DMC"
    assert high_score["score"] == 60000

    # query scores and make sure all IDs in each table row are non-null.
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
    for entry in content:
        assert entry["initials"] is not None
        assert entry["score"] is not None
    # clear high scores, then make sure they are actually cleared.
    response = client.post("/clear_scores")
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    content = response.json()
    assert content == []


def test_addscore_score_but_no_initials(client: TestClient) -> None:
    response = client.post("/add_score?initials=BCC")
    assert response.status_code == 422  # unprocessable content


def test_addscore_initials_but_no_score(client: TestClient) -> None:
    response = client.post("/add_score?score=120000")
    assert response.status_code == 422  # unprocessable content


def test_three_highscores_returns_sorted(client: TestClient) -> None:
    # start by clearing out existing high scores
    response = client.post("/clear_scores")
    assert response.status_code == 200

    # add one higher score
    response = client.post("/add_score?initials=AMC&score=12000")
    assert response.status_code == 200

    # add one lower score and make sure scores are sorted descending
    response = client.post("/add_score?initials=BCC&score=10000")
    assert response.status_code == 200

    response = client.post("/add_score?initials=DMC&score=11000")
    assert response.status_code == 200
    response = client.get("/high_scores")
    assert response.status_code == 200
    expected = [
        {"initials": "AMC", "score": 12000},
        {"initials": "DMC", "score": 11000},
        {"initials": "BCC", "score": 10000},
    ]
    assert response.json() == expected


def test_eleven_highscores_top_ten(client: TestClient) -> None:
    # start by clearing out existing high scores
    response = client.post("/clear_scores")
    assert response.status_code == 200

    for i in range(11):
        initials = chr(65 + i) * 3
        score = 10000 * (i + 1)
        response = client.post(f"/add_score?initials={initials}&score={score}")
        assert response.status_code == 200

    response = client.get("/high_scores")
    assert response.status_code == 200
    expected = [
        {"initials": "KKK", "score": 110000},
        {"initials": "JJJ", "score": 100000},
        {"initials": "III", "score": 90000},
        {"initials": "HHH", "score": 80000},
        {"initials": "GGG", "score": 70000},
        {"initials": "FFF", "score": 60000},
        {"initials": "EEE", "score": 50000},
        {"initials": "DDD", "score": 40000},
        {"initials": "CCC", "score": 30000},
        {"initials": "BBB", "score": 20000},
    ]
    assert response.json() == expected
