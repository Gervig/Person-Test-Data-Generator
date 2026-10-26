import pytest
from pydantic import TypeAdapter, ValidationError

from app.models.person import CprNumber, MobileNumber, Person

cpr_adapter = TypeAdapter(CprNumber)
mobile_adapter = TypeAdapter(MobileNumber)

# Positive tests

# Test valid_person fixture works
def test_valid_person(valid_person):  # fixture in tests/conftest.py
    assert isinstance(valid_person, Person)
    assert valid_person.first_name == "John"
    assert valid_person.gender == "male"


@pytest.mark.parametrize(
    "gender",
    [
        "male",
        "female",
    ]
)
def test_valid_person_gender(valid_person_data, gender):
    valid_person_data["gender"] = gender
    Person(**valid_person_data)


@pytest.mark.parametrize(
    "cpr",
    [
        "1212124321",
        "0102034567",
    ]
)
def test_valid_cpr_format(cpr):
    assert cpr_adapter.validate_python(cpr) == cpr


@pytest.mark.parametrize(
    "phone",
    [
        "42102030",
        "30123456",
        "60123456",
        "34212345",
    ]
)
def test_valid_mobile_phone_number(phone):
    assert mobile_adapter.validate_python(phone) == phone


# Negative tests

@pytest.mark.parametrize(
    "gender",
    [
        "",
        "Male",
        "other",
        "m",
    ]
)
def test_invalid_gender(valid_person_data, gender):
    valid_person_data["gender"] = gender
    with pytest.raises(ValidationError):
        Person(**valid_person_data)


@pytest.mark.parametrize(
    "cpr",
    [
        "12345",        # Too short
        "12345678901",  # Too long
        "abcdefghij",   # Not digits
        "12345abcde",   # Contains letters
        "123456789²",   # Non-ASCII digit
    ],
)
def test_invalid_cpr_format(cpr):
    with pytest.raises(ValidationError, match="Must be exactly 10 digits"):
        cpr_adapter.validate_python(cpr)


# CPR and date of birth must agree (fixture has date_of_birth 1990-01-17)
@pytest.mark.parametrize(
    "cpr", 
    [
        "1801901234", 
        "1702901234", 
        "1701911234",
    ]
)
def test_cpr_date_of_birth_mismatch(valid_person_data, cpr):
    valid_person_data["cpr"] = cpr
    with pytest.raises(ValidationError, match="CPR date of birth mismatch"):
        Person(**valid_person_data)


@pytest.mark.parametrize(
    "phone",
    [
        "1234567",     # Too short
        "123456789",   # Too long
        "abcdefgh",    # Not digits
        "4210203²",    # Non-ASCII digit
    ]
)
def test_invalid_mobile_phone_length_or_digits(phone):
    with pytest.raises(ValidationError, match="Must be exactly 8 digits"):
        mobile_adapter.validate_python(phone)


def test_invalid_mobile_phone_prefix():
    with pytest.raises(ValidationError, match="invalid prefix"):
        mobile_adapter.validate_python("12345678")