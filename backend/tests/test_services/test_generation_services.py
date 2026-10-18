from random import Random

from app.models.postal_code import PostalCode
from app.repositories import postal_code_repository
from app.services.address_service import generate_address
from app.services.person_service import generate_person


def test_generated_address_passes_model_validation(monkeypatch) -> None:
    monkeypatch.setattr(
        postal_code_repository,
        "get_random",
        lambda: PostalCode(postal_code="2200", town="København N"),
    )

    address = generate_address(Random(4))

    assert address.postal_code.postal_code == "2200"


def test_generated_person_passes_model_validation(monkeypatch) -> None:
    monkeypatch.setattr(
        postal_code_repository,
        "get_random",
        lambda: PostalCode(postal_code="2200", town="København N"),
    )

    person = generate_person(Random(5))

    assert person.cpr[:6] == person.date_of_birth.strftime("%d%m%y")
    assert person.address.postal_code.postal_code == "2200"
