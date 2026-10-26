from datetime import date
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, model_validator

from app.models.address import Address
from app.models.phone_prefixes import ALLOWED_PHONE_PREFIXES


def _digits(length: int) -> AfterValidator:
    def check(value: str) -> str:
        if len(value) != length or not (value.isascii() and value.isdigit()):
            raise ValueError(f"Must be exactly {length} digits")
        return value

    return AfterValidator(check)


def _check_phone_prefix(value: str) -> str:
    if not value.startswith(ALLOWED_PHONE_PREFIXES):
        raise ValueError("Mobile phone number has an invalid prefix")
    return value


Gender = Literal["male", "female"]
CprNumber = Annotated[str, _digits(10)]
MobileNumber = Annotated[str, _digits(8), AfterValidator(_check_phone_prefix)]


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    date_of_birth: date
    cpr: CprNumber
    mobile_phone_number: MobileNumber
    address: Address

    @model_validator(mode="after")
    def _cpr_matches_date_of_birth(self) -> "Person":
        
        date_of_birth = self.date_of_birth
        # extract day, month and year digits from date_of_birth
        # builds a string in format "ddmmyy"
        expected_date = (
            f"{date_of_birth.day:02d}" # 02d means 2 digits, 0 padded if needed
            f"{date_of_birth.month:02d}" # same thing here for month
            f"{date_of_birth.year % 100:02d}" # year % 100 means last two digits of year
        )
        if self.cpr[:6] != expected_date:
            raise ValueError("CPR date of birth mismatch")

        return self


class PersonList(BaseModel):
    persons: list[Person]