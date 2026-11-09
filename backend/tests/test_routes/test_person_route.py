import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.person import PersonList
from app.routers import person


client = TestClient(app)

@pytest.fixture(autouse=True)
def fake_generate_persons(monkeypatch, valid_person):
    monkeypatch.setattr(
        person,
        "generate_persons",
        lambda count: PersonList(persons=[valid_person] * count),
    )

@pytest.mark.parametrize(
    "count, expected_status",
    [
        pytest.param("-1", 422, id="below-range-negative"),
        pytest.param("0", 422, id="below-range-zero"),
        pytest.param("1", 422, id="one-below-lower-boundary"),
        pytest.param("2", 200, id="lower-boundary"),
        pytest.param("3", 200, id="one-above-lower-boundary"),
        pytest.param("50", 200, id="inside-range"),
        pytest.param("99", 200, id="one-below-upper-boundary"),
        pytest.param("100", 200, id="upper-boundary"),
        pytest.param("101", 422, id="one-above-upper-boundary"),
        pytest.param("abc", 422, id="wrong-type"),
    ],
)
def test_persons_count_bounds(count, expected_status):
    response = client.get(f"/persons?count={count}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert len(response.json()["persons"]) == int(count)
