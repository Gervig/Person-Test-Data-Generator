from datetime import date

from pydantic import BaseModel


class Name(BaseModel):
    first_name: str
    last_name: str
    gender: str


class NameAndBirthDate(Name):
    date_of_birth: date


class Cpr(BaseModel):
    cpr: str


class CprAndName(BaseModel):
    first_name: str
    last_name: str
    gender: str
    cpr: str


class CprNameAndBirthDate(CprAndName):
    date_of_birth: date


class MobilePhoneNumber(BaseModel):
    mobile_phone_number: str