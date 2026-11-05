from datetime import date

import pytest
from pydantic import ValidationError

from app.models.person import Person


def person_with(data: dict, **overrides) -> Person:
    return Person(**{**data, **overrides})


def assert_field_rejected(
    data: dict, field: str, value, message: str | None = None
) -> None:
    """Assert that exactly `field` was rejected, optionally with a message."""
    with pytest.raises(ValidationError) as exc_info:
        person_with(data, **{field: value})
    errors = exc_info.value.errors()
    assert [e["loc"] for e in errors] == [(field,)]
    if message is not None:
        assert message in errors[0]["msg"]


# Whole object

def test_valid_person(valid_person):
    assert isinstance(valid_person, Person)
    assert valid_person.first_name == "John"
    assert valid_person.gender == "male"


@pytest.mark.parametrize("field", list(Person.model_fields))
def test_missing_required_field_is_rejected(valid_person_data, field):
    data = {k: v for k, v in valid_person_data.items() if k != field}
    with pytest.raises(ValidationError) as exc_info:
        Person(**data)
    assert [e["loc"] for e in exc_info.value.errors()] == [(field,)]


@pytest.mark.parametrize(
    "field, value",
    [
        pytest.param("first_name", 123, id="first_name-int"),
        pytest.param("last_name", None, id="last_name-none"),
        pytest.param("date_of_birth", None, id="date_of_birth-none"),
        pytest.param("cpr", 1701901234, id="cpr-int"),
        pytest.param("mobile_phone_number", 42102030, id="mobile-int"),
        pytest.param("address", "not-an-address", id="address-string"),
    ],
)
def test_wrong_type_is_rejected(valid_person_data, field, value):
    assert_field_rejected(valid_person_data, field, value)


# Names

@pytest.mark.parametrize(
    "name",
    [
        pytest.param("John", id="ascii"),
        pytest.param("Søren", id="danish-letters"),
        pytest.param("Anne-Marie", id="double-barrelled"),
    ],
)
def test_valid_names(valid_person_data, name):
    person = person_with(valid_person_data, first_name=name, last_name=name)
    assert person.first_name == name
    assert person.last_name == name


# Gender

@pytest.mark.parametrize("gender", ["male", "female"])
def test_valid_gender(valid_person_data, gender):
    assert person_with(valid_person_data, gender=gender).gender == gender


@pytest.mark.parametrize(
    "gender",
    [
        pytest.param("Male", id="wrong-case"),
        pytest.param("other", id="unlisted-value"),
        pytest.param("", id="empty"),
        pytest.param("male ", id="trailing-whitespace"),
    ],
)
def test_invalid_gender(valid_person_data, gender):
    assert_field_rejected(valid_person_data, "gender", gender)


# Date of birth

@pytest.mark.parametrize(
    "value",
    [
        pytest.param("1990-02-30", id="impossible-date"),
        pytest.param("not-a-date", id="unparseable-string"),
    ],
)
def test_invalid_date_of_birth(valid_person_data, value):
    assert_field_rejected(valid_person_data, "date_of_birth", value)


# CPR format. Valid CPRs must match the date of birth, so the valid
# partitions live in the date-of-birth test below.

@pytest.mark.parametrize(
    "cpr",
    [
        pytest.param("", id="empty"),
        pytest.param("170190123", id="one-below-length"),
        pytest.param("17019012345", id="one-above-length"),
        pytest.param("abcdefghij", id="letters-only"),
        pytest.param("12345abcde", id="letters-mixed-with-digits"),
        pytest.param("123456789²", id="non-ascii-digit"),
    ],
)
def test_invalid_cpr_format(valid_person_data, cpr):
    assert_field_rejected(
        valid_person_data, "cpr", cpr, "Must be exactly 10 digits"
    )


# CPR vs date of birth

@pytest.mark.parametrize(
    "dob, cpr",
    [
        pytest.param(date(1990, 1, 17), "1701901234", id="regular-date"),
        pytest.param(date(2005, 1, 1), "0101051234", id="leading-zeros"),
        pytest.param(date(2000, 2, 29), "2902001234", id="leap-day"),
        pytest.param(date(1999, 12, 31), "3112991234", id="last-day-of-year"),
    ],
)
def test_cpr_matches_date_of_birth(valid_person_data, dob, cpr):
    person = person_with(valid_person_data, date_of_birth=dob, cpr=cpr)
    assert person.cpr == cpr


# Fixture date of birth is 1990-01-17, so each case differs in one component.
@pytest.mark.parametrize(
    "cpr",
    [
        pytest.param("1801901234", id="day-differs"),
        pytest.param("1702901234", id="month-differs"),
        pytest.param("1701911234", id="year-differs"),
    ],
)
def test_cpr_date_of_birth_mismatch(valid_person_data, cpr):
    with pytest.raises(ValidationError, match="CPR date of birth mismatch"):
        person_with(valid_person_data, cpr=cpr)


# Mobile phone number

@pytest.mark.parametrize(
    "phone",
    [
        pytest.param("21234567", id="one-digit-prefix"),
        pytest.param("30123456", id="two-digit-prefix"),
        pytest.param("34212345", id="three-digit-prefix"),
        pytest.param("82912345", id="last-listed-prefix"),
    ],
)
def test_valid_mobile_phone_number(valid_person_data, phone):
    person = person_with(valid_person_data, mobile_phone_number=phone)
    assert person.mobile_phone_number == phone


@pytest.mark.parametrize(
    "phone",
    [
        pytest.param("", id="empty"),
        pytest.param("4210203", id="one-below-length"),
        pytest.param("421020301", id="one-above-length"),
        pytest.param("abcdefgh", id="letters"),
        pytest.param("4210203²", id="non-ascii-digit"),
    ],
)
def test_invalid_mobile_phone_format(valid_person_data, phone):
    assert_field_rejected(
        valid_person_data,
        "mobile_phone_number",
        phone,
        "Must be exactly 8 digits",
    )


@pytest.mark.parametrize(
    "phone",
    [
        pytest.param("12345678", id="unlisted-first-digit"),
        pytest.param("34012345", id="near-miss-three-digit-prefix"),
        pytest.param("80123456", id="near-miss-two-digit-prefix"),
    ],
)
def test_invalid_mobile_phone_prefix(valid_person_data, phone):
    assert_field_rejected(
        valid_person_data, "mobile_phone_number", phone, "invalid prefix"
    )