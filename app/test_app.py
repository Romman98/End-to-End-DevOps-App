import pytest
from app import app

# ---------- FIXTURES ----------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------- TEST HOME ----------
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"I am working!!" in res.data


# ---------- TEST NEW REVIEW ----------
def test_new_review_success(client, mocker):
    # Mock DB functions
    mocker.patch("app.checkEntry", return_value=False)
    mocker.patch("app.queryFunc", return_value=True)

    response = client.post(
        "/review/new",
        json={"name": "John", "rating": "5"}
    )

    assert response.status_code == 200
    assert b"Data Inserted Successfully" in response.data


def test_new_review_duplicate(client, mocker):
    mocker.patch("app.checkEntry", return_value=True)

    response = client.post(
        "/review/new",
        json={"name": "John", "rating": "5"}
    )

    assert response.status_code == 200
    assert b"Data already exists" in response.data


# ---------- TEST GET ALL REVIEWS ----------
def test_get_reviews(client, mocker):
    mock_data = [["John", "5"]]
    mocker.patch("app.queryFunc", return_value=mock_data)

    response = client.get("/review")

    assert response.status_code == 200
    assert response.json == {"results": mock_data}


# ---------- TEST FILTER BY NAME ----------
def test_get_review_by_name(client, mocker):
    mocker.patch("app.queryFunc", return_value=[["John", "5"]])

    response = client.get("/review/query?name=John")

    assert response.status_code == 200
    assert response.json["Result"] == [["John", "5"]]


# ---------- TEST FILTER BY RATING ----------
def test_get_review_by_rating(client, mocker):
    mocker.patch("app.queryFunc", return_value=[("Ali", "4")])

    response = client.get("/review/query?rating=4")

    assert response.status_code == 200
    assert response.json["Result"] == [["Ali", "4"]]


# ---------- TEST INVALID FILTER ----------
def test_get_review_invalid(client):
    response = client.get("/review/query")
    assert response.status_code == 200
    assert "Incorrect input" in response.json["Result"]
