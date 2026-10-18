from random import Random

from app import generators
from app.dtos.person_dto import (
    CprAndNameDTO,
    CprNameAndBirthDateDTO,
    CprDTO,
    NameAndBirthDateDTO,
    NameDTO,
    PersonDTO,
)
from app.models.person import Person
from app.services.address_service import create_address


def generate_name(rng: Random | None = None) -> NameDTO:
    return NameDTO(**generators.random_name(rng))


def generate_name_and_birth_date(
    rng: Random | None = None,
) -> NameAndBirthDateDTO:
    name = generators.random_name(rng)
    return NameAndBirthDateDTO(
        **name,
        date_of_birth=generators.random_date_of_birth(rng),
    )


def generate_cpr(rng: Random | None = None) -> CprDTO:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return CprDTO(
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng)
    )


def generate_cpr_and_name(rng: Random | None = None) -> CprAndNameDTO:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return CprAndNameDTO(
        **name,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
    )


def generate_cpr_name_and_birth_date(
    rng: Random | None = None,
) -> CprNameAndBirthDateDTO:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    return CprNameAndBirthDateDTO(
        **name,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
        date_of_birth=date_of_birth,
    )


def generate_mobile_phone_number(rng: Random | None = None) -> str:
    return generators.random_phone_number(rng)


def generate_person(rng: Random | None = None) -> PersonDTO:
    name = generators.random_name(rng)
    date_of_birth = generators.random_date_of_birth(rng)
    person = Person(
        **name,
        date_of_birth=date_of_birth,
        cpr=generators.random_cpr(date_of_birth, name["gender"], rng),
        mobile_phone_number=generators.random_phone_number(rng),
        address=create_address(rng),
    )
    return PersonDTO.model_validate(person, from_attributes=True)


def generate_persons(count: int, rng: Random | None = None) -> list[PersonDTO]:
    return [generate_person(rng) for _ in range(count)]
