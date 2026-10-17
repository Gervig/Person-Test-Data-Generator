import pytest
from pydantic import ValidationError
from datetime import date

from app.models.person import Person

#TODO: add valid Postal Code and Address from fixture

# Positive tests
@pytest.mark.parametrize(
    "first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number",
    [
        ("john", "doe", "male", date(2026, 10, 17), "1710263075", "42102030")
    ],
)
def test_valid_person(first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number, valid_address): # valid_address from fixture in tests/conftest.py
    Person(first_name=first_name, last_name=last_name, gender=gender, date_of_birth=date_of_birth, cpr=cpr, mobile_phone_number=mobile_phone_number, address=valid_address)


# Negative tests
@pytest.mark.parametrize(
    "first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number",
    [
        (1234, 5678, "tomato", "50-30-2030", "171000-3075", "45102030")
    ],
)
def test_invalid_person(first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number, valid_address): # valid_address from fixture in tests/conftest.py
    with pytest.raises(ValidationError):
        Person(first_name=first_name, last_name=last_name, gender=gender, date_of_birth=date_of_birth, cpr=cpr, mobile_phone_number=mobile_phone_number, address=valid_address)

