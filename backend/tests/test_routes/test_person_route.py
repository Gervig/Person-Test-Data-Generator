from fastapi.testclient import TestClient

from app.main import app
from app.models.person import PersonList
from app.routers import person


client = TestClient(app)


def test_persons_count_bounds(monkeypatch) -> None:
    monkeypatch.setattr(
        person,
        "generate_persons",
        lambda count: PersonList(persons=[]),
    )

    assert client.get("/persons?count=1").status_code == 422
    assert client.get("/persons?count=101").status_code == 422
    assert client.get("/persons?count=2").status_code == 200
    assert client.get("/persons?count=100").status_code == 200
