from fastapi.testclient import TestClient

from app.main import app
from app.models.postal_code import PostalCode
from app.repositories import postal_code_repository


client = TestClient(app)


def test_api_response_keys_and_types(monkeypatch) -> None:
    fixed_postal_code = PostalCode(
        postal_code="2200",
        town="København N",
    )
    monkeypatch.setattr(
        postal_code_repository,
        "get_random",
        lambda: fixed_postal_code,
    )
    monkeypatch.setattr(
        postal_code_repository,
        "get_all",
        lambda: [fixed_postal_code],
    )

    responses = {
        "/cpr": client.get("/cpr"),
        "/name": client.get("/name"),
        "/name-and-birth-date": client.get("/name-and-birth-date"),
        "/cpr-and-name": client.get("/cpr-and-name"),
        "/cpr-name-and-birth-date": client.get("/cpr-name-and-birth-date"),
        "/address": client.get("/address"),
        "/mobile-phone-number": client.get("/mobile-phone-number"),
        "/person": client.get("/person"),
        "/persons?count=2": client.get("/persons?count=2"),
        "/postal-codes": client.get("/postal-codes"),
    }

    assert all(response.status_code == 200 for response in responses.values())

    cpr = responses["/cpr"].json()
    assert set(cpr) == {"cpr"}
    assert isinstance(cpr["cpr"], str)

    name = responses["/name"].json()
    assert set(name) == {"first_name", "last_name", "gender"}
    assert all(isinstance(name[key], str) for key in name)

    name_and_birth_date = responses["/name-and-birth-date"].json()
    assert set(name_and_birth_date) == {
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
    }
    assert all(isinstance(name_and_birth_date[key], str) for key in name_and_birth_date)

    cpr_and_name = responses["/cpr-and-name"].json()
    assert set(cpr_and_name) == {"first_name", "last_name", "gender", "cpr"}
    assert all(isinstance(cpr_and_name[key], str) for key in cpr_and_name)

    cpr_name_and_birth_date = responses["/cpr-name-and-birth-date"].json()
    assert set(cpr_name_and_birth_date) == {
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "cpr",
    }
    assert all(
        isinstance(cpr_name_and_birth_date[key], str)
        for key in cpr_name_and_birth_date
    )

    address = responses["/address"].json()
    assert set(address) == {"street", "number", "floor", "door", "postal_code"}
    assert set(address["postal_code"]) == {"postal_code", "town_name"}
    assert all(isinstance(address[key], str) for key in address if key != "postal_code")
    assert all(isinstance(address["postal_code"][key], str) for key in address["postal_code"])

    mobile_phone_number = responses["/mobile-phone-number"].json()
    assert set(mobile_phone_number) == {"mobile_phone_number"}
    assert isinstance(mobile_phone_number["mobile_phone_number"], str)

    person = responses["/person"].json()
    assert set(person) == {
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "cpr",
        "mobile_phone_number",
        "address",
    }
    assert all(isinstance(person[key], str) for key in person if key != "address")
    assert set(person["address"]) == {
        "street",
        "number",
        "floor",
        "door",
        "postal_code",
    }
    assert set(person["address"]["postal_code"]) == {"postal_code", "town_name"}

    persons = responses["/persons?count=2"].json()
    assert set(persons) == {"persons"}
    assert isinstance(persons["persons"], list)
    assert len(persons["persons"]) == 2
    assert all(set(item) == set(person) for item in persons["persons"])

    postal_codes = responses["/postal-codes"].json()
    assert isinstance(postal_codes, list)
    assert len(postal_codes) == 1
    assert set(postal_codes[0]) == {"postal_code", "town"}
    assert all(isinstance(value, str) for value in postal_codes[0].values())
