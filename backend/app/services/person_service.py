from random import Random

from app import generators
from app.models.person import Person
from app.services.address_service import create_address


def generate_person(rng: Random | None = None) -> Person:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return Person(
        **name,
        date_of_birth=date_of_birth,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
        mobile_phone_number=generators.random_phone_number(rng),
        address=create_address(rng),
    )


def generate_persons(count: int, rng: Random | None = None) -> list[Person]:
    return [generate_person(rng) for _ in range(count)]