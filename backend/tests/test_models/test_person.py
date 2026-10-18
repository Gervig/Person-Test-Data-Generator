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


# Test valid gender  
@pytest.mark.parametrize(
    "gender",
    [
        "male", 
        "female"
    ],
)
def test_valid_person_gender(valid_person_data, gender): # valid_person_data from fixture in tests/conftest.py
    valid_person_data["gender"] = gender

    Person(**valid_person_data) # Python unpacking operator ** passes dictionary inputs from fixture

# Test CPR format, length 10 and numeric
@pytest.mark.parametrize(
    "cpr",
    [
        "1212124321",
        "0102034567",
    ],
)
def test_valid_cpr_format(cpr):
    # call the specific class method validation
    # cpr has 2 validation methods, test one thing at a time
    assert Person.validate_cpr_format(cpr) == cpr

# Negative tests

# Invalid CPR format
@pytest.mark.parametrize(
    "cpr",
    [
        "12345",          # Too short
        "12345678901",    # Too long
        "abcdefghij",     # Not digits
        "12345abcde",     # Contains letters
    ],
)
def test_invalid_cpr_format(cpr):
    with pytest.raises(ValueError, match="CPR number must be exactly 10 digits"):
        Person.validate_cpr_format(cpr)
