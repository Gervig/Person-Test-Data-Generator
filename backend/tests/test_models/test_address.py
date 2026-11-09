import pytest
from pydantic import ValidationError

from app.models.address import Address


def address_with(data: dict, **overrides) -> Address:
    return Address(**{**data, **overrides})


def assert_field_rejected(
    data: dict, field: str, value, message: str | None = None
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        address_with(data, **{field: value})
    errors = exc_info.value.errors()
    assert [e["loc"] for e in errors] == [(field,)]
    if message is not None:
        assert message in errors[0]["msg"]


# Whole object

def test_valid_address(valid_address):
    assert isinstance(valid_address, Address)
    assert valid_address.street == "Guldbergsgade"
    assert valid_address.number == "29"


def test_model_dump_round_trip(valid_address):
    assert Address(**valid_address.model_dump()) == valid_address


def test_postal_code_is_serialized_with_town_name(valid_address):
    assert valid_address.model_dump()["postal_code"] == {
        "postal_code": "2200",
        "town_name": "København N",
    }


@pytest.mark.parametrize("field", list(Address.model_fields))
def test_missing_required_field_is_rejected(valid_address_data, field):
    data = {k: v for k, v in valid_address_data.items() if k != field}
    with pytest.raises(ValidationError) as exc_info:
        Address(**data)
    assert [e["loc"] for e in exc_info.value.errors()] == [(field,)]


@pytest.mark.parametrize(
    "field, value",
    [
        pytest.param("street", 123, id="street-int"),
        pytest.param("number", 29, id="number-int"),
        pytest.param("floor", 1, id="floor-int"),
        pytest.param("door", 5, id="door-int"),
    ],
)
def test_wrong_type_is_rejected(valid_address_data, field, value):
    assert_field_rejected(valid_address_data, field, value)


# Street

@pytest.mark.parametrize(
    "street",
    [
        pytest.param("Guldbergsgade", id="ascii"),
        pytest.param("Østerbrogade", id="danish-letters"),
        pytest.param("H.C. Andersens Boulevard", id="punctuation-and-spaces"),
    ],
)
def test_valid_street(valid_address_data, street):
    assert address_with(valid_address_data, street=street).street == street


# Number

@pytest.mark.parametrize(
    "number",
    [
        pytest.param("1", id="lower-boundary"),
        pytest.param("29", id="typical"),
        pytest.param("999", id="upper-boundary"),
        pytest.param("29A", id="with-suffix"),
        pytest.param("999Z", id="max-with-suffix"),
    ],
)
def test_valid_number(valid_address_data, number):
    assert address_with(valid_address_data, number=number).number == number


@pytest.mark.parametrize(
    "number",
    [
        pytest.param("", id="empty"),
        pytest.param("A", id="letter-only"),
        pytest.param("0", id="zero"),
        pytest.param("01", id="leading-zero"),
        pytest.param("1000", id="above-upper-boundary"),
        pytest.param("29a", id="lowercase-suffix"),
        pytest.param("29AB", id="two-letter-suffix"),
        pytest.param("2A9", id="letter-in-the-middle"),
        pytest.param("29 ", id="trailing-space"),
        pytest.param("\u0663", id="non-ascii-digit"),
    ],
)
def test_invalid_number(valid_address_data, number):
    assert_field_rejected(
        valid_address_data, "number", number, "Address number must be"
    )


# Floor

@pytest.mark.parametrize(
    "floor",
    [
        pytest.param("st", id="ground-floor"),
        pytest.param("1", id="lower-boundary"),
        pytest.param("99", id="upper-boundary"),
    ],
)
def test_valid_floor(valid_address_data, floor):
    assert address_with(valid_address_data, floor=floor).floor == floor


@pytest.mark.parametrize(
    "floor",
    [
        pytest.param("", id="empty"),
        pytest.param("0", id="zero"),
        pytest.param("01", id="leading-zero"),
        pytest.param("100", id="above-upper-boundary"),
        pytest.param("ST", id="ground-floor-wrong-case"),
        pytest.param("1a", id="digit-and-letter"),
        pytest.param("-1", id="negative"),
        pytest.param("\u0663", id="non-ascii-digit"),
    ],
)
def test_invalid_floor(valid_address_data, floor):
    assert_field_rejected(
        valid_address_data, "floor", floor, "Address floor must be"
    )


# Door

@pytest.mark.parametrize(
    "door",
    [
        pytest.param("th", id="th"),
        pytest.param("mf", id="mf"),
        pytest.param("tv", id="tv"),
        pytest.param("1", id="number-lower-boundary"),
        pytest.param("50", id="number-upper-boundary"),
        pytest.param("c3", id="letter-one-digit"),
        pytest.param("d-14", id="letter-dash-two-digits"),
        pytest.param("a123", id="letter-three-digits"),
        pytest.param("b-999", id="letter-dash-three-digits"),
    ],
)
def test_valid_door(valid_address_data, door):
    assert address_with(valid_address_data, door=door).door == door


@pytest.mark.parametrize(
    "door",
    [
        pytest.param("", id="empty"),
        pytest.param("0", id="zero"),
        pytest.param("01", id="leading-zero"),
        pytest.param("51", id="above-number-boundary"),
        pytest.param("TH", id="special-word-wrong-case"),
        pytest.param("c", id="letter-only"),
        pytest.param("c-", id="letter-dash-no-digits"),
        pytest.param("C3", id="uppercase-letter"),
        pytest.param("c1234", id="four-digits"),
        pytest.param("c--3", id="double-dash"),
        pytest.param("3c", id="digit-before-letter"),
        pytest.param("c3x", id="trailing-letter"),
        pytest.param("\u0663", id="non-ascii-digit-number"),
        pytest.param("c\u0663", id="non-ascii-digit-suffix"),
    ],
)
def test_invalid_door(valid_address_data, door):
    assert_field_rejected(
        valid_address_data, "door", door, "Address door must be"
    )


# Postal code (nested)

def test_postal_code_accepted_as_dict(valid_address_data):
    postal_code = {"postal_code": "8000", "town_name": "Aarhus C"}
    address = address_with(valid_address_data, postal_code=postal_code)
    assert address.postal_code.town == "Aarhus C"


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("2200", id="string"),
        pytest.param(None, id="none"),
    ],
)
def test_postal_code_wrong_type_is_rejected(valid_address_data, value):
    assert_field_rejected(valid_address_data, "postal_code", value)


def test_nested_invalid_postal_code_is_rejected(valid_address_data):
    invalid = {"postal_code": "123", "town_name": "København N"}
    with pytest.raises(ValidationError) as exc_info:
        address_with(valid_address_data, postal_code=invalid)
    locations = [e["loc"] for e in exc_info.value.errors()]
    assert locations == [("postal_code", "postal_code")]
