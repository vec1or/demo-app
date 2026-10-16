from app import app


def test_home():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200
    assert b"Hello from DevOps demo app" in response.data