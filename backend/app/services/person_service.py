from random import Random

from app import generators
from app.models.person import (
    Cpr,
    CprAndName,
    CprNameAndBirthDate,
    Name,
    NameAndBirthDate,
    Person,
)
from app.services.address_service import create_address


def generate_name(rng: Random | None = None) -> Name:
    return Name(**generators.random_name(rng))


def generate_name_and_birth_date(
    rng: Random | None = None,
) -> NameAndBirthDate:
    name = generators.random_name(rng)
    return NameAndBirthDate(
        **name,
        date_of_birth=generators.random_date_of_birth(rng),
    )


def generate_cpr(rng: Random | None = None) -> Cpr:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return Cpr(
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng)
    )


def generate_cpr_and_name(rng: Random | None = None) -> CprAndName:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return CprAndName(
        **name,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
    )


def generate_cpr_name_and_birth_date(
    rng: Random | None = None,
) -> CprNameAndBirthDate:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return CprNameAndBirthDate(
        **name,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
        date_of_birth=date_of_birth,
    )


def generate_mobile_phone_number(rng: Random | None = None) -> str:
    return generators.random_phone_number(rng)


def generate_person(rng: Random | None = None) -> Person:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    person = Person(
        **name,
        date_of_birth=date_of_birth,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
        mobile_phone_number=generators.random_phone_number(rng),
        address=create_address(rng),
    )
    return person


def generate_persons(count: int, rng: Random | None = None) -> list[Person]:
    return [generate_person(rng) for _ in range(count)]
