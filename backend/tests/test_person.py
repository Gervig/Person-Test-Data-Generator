import pytest
from pydantic import ValidationError
from datetime import date

from app.models import Person

#TODO: add valid Postal Code and Address from fixture

# Positive tests
@pytest.mark.parametrize(
    "first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number",
    [
        ("john", "doe", "male", "17-10-2000", "171000-3075", "42102030")
    ],
)
def test_valid_person(first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number):
    Person(first_name=first_name, last_name=last_name, gender=gender, date_of_birth=date_of_birth, cpr=cpr, mobile_phone_number=mobile_phone_number)
    
# Negative tests
@pytest.mark.parametrize(
    "first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number",
    [
        ("john", "doe", "male", "17-10-2000", "171000-3075", "42102030")
    ],
)
def test_valid_person(first_name, last_name, gender, date_of_birth, cpr, mobile_phone_number):
    with pytest.raises(ValidationError):
        Person(first_name=first_name, last_name=last_name, gender=gender, date_of_birth=date_of_birth, cpr=cpr, mobile_phone_number=mobile_phone_number)
    
