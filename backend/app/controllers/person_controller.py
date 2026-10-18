from app.models.person import (
    Cpr,
    CprAndName,
    CprNameAndBirthDate,
    Name,
    NameAndBirthDate,
    Person,
    PersonList,
)
from app.services import person_service


def generate_name() -> Name:
    return person_service.generate_name()


def generate_name_and_birth_date() -> NameAndBirthDate:
    return person_service.generate_name_and_birth_date()


def generate_cpr() -> Cpr:
    return person_service.generate_cpr()


def generate_cpr_and_name() -> CprAndName:
    return person_service.generate_cpr_and_name()


def generate_cpr_name_and_birth_date() -> CprNameAndBirthDate:
    return person_service.generate_cpr_name_and_birth_date()


def generate_mobile_phone_number() -> str:
    return person_service.generate_mobile_phone_number()


def generate_person() -> Person:
    return person_service.generate_person()


def generate_persons(count: int) -> PersonList:
    return PersonList(persons=person_service.generate_persons(count))
