from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_reports_that_the_api_is_running() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Personal Test Data Generator API is running!"}
