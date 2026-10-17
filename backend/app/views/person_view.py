from datetime import date

from pydantic import BaseModel

from app.views.address_view import AddressView


class NameView(BaseModel):
    first_name: str
    last_name: str
    gender: str


class NameAndBirthDateView(NameView):
    date_of_birth: date


class CprView(BaseModel):
    cpr: str


class CprAndNameView(NameView):
    cpr: str


class CprNameAndBirthDateView(NameAndBirthDateView):
    cpr: str


class PersonView(NameAndBirthDateView):
    cpr: str
    address: AddressView
    mobile_phone_number: str


class BulkPersonView(BaseModel):
    persons: list[PersonView]
