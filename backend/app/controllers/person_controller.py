from app.dtos.person_dto import (
    BulkPersonDTO,
    CprAndNameDTO,
    CprNameAndBirthDateDTO,
    CprDTO,
    NameAndBirthDateDTO,
    NameDTO,
    PersonDTO,
)
from app.services import person_service


def generate_name() -> NameDTO:
    return person_service.generate_name()


def generate_name_and_birth_date() -> NameAndBirthDateDTO:
    return person_service.generate_name_and_birth_date()


def generate_cpr() -> CprDTO:
    return person_service.generate_cpr()


def generate_cpr_and_name() -> CprAndNameDTO:
    return person_service.generate_cpr_and_name()


def generate_cpr_name_and_birth_date() -> CprNameAndBirthDateDTO:
    return person_service.generate_cpr_name_and_birth_date()


def generate_mobile_phone_number() -> str:
    return person_service.generate_mobile_phone_number()


def generate_person() -> PersonDTO:
    return person_service.generate_person()


def generate_persons(count: int) -> BulkPersonDTO:
    return BulkPersonDTO(persons=person_service.generate_persons(count))
