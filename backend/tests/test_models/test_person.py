import pytest
from pydantic import ValidationError
from datetime import date

from app.models.person import Person

#TODO: test each input in its own test function with parametrized partitions

# Positive tests

# Test valid_person fixture works
def test_valid_person(valid_person): # valid_person from fixture in tests/conftest.py
    assert isinstance(valid_person, Person)
    assert valid_person.first_name == "John"
    assert valid_person.gender == "male"


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

