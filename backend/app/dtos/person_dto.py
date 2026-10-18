from datetime import date

from pydantic import BaseModel

from app.dtos.address_dto import AddressDTO


class NameDTO(BaseModel):
    first_name: str
    last_name: str
    gender: str


class NameAndBirthDateDTO(NameDTO):
    date_of_birth: date


class CprDTO(BaseModel):
    cpr: str


class CprAndNameDTO(NameDTO):
    cpr: str


class CprNameAndBirthDateDTO(NameAndBirthDateDTO):
    cpr: str


class PersonDTO(NameAndBirthDateDTO):
    cpr: str
    address: AddressDTO
    mobile_phone_number: str


class BulkPersonDTO(BaseModel):
    persons: list[PersonDTO]
