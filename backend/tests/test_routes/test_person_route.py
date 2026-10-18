from fastapi.testclient import TestClient

from app.dtos.person_dto import BulkPersonDTO
from app.main import app
from app.routes import person


client = TestClient(app)


def test_persons_count_bounds(monkeypatch) -> None:
    monkeypatch.setattr(
        person,
        "generate_persons",
        lambda count: BulkPersonDTO(persons=[]),
    )

    assert client.get("/persons?count=0").status_code == 422
    assert client.get("/persons?count=101").status_code == 422
    assert client.get("/persons?count=100").status_code == 200
