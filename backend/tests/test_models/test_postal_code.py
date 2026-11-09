import pytest
from pydantic import ValidationError

from app.models.postal_code import PostalCode


def postal_code_with(data: dict, **overrides) -> PostalCode:
    return PostalCode(**{**data, **overrides})


def assert_field_rejected(
    data: dict, field: str, value, message: str | None = None
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        postal_code_with(data, **{field: value})
    errors = exc_info.value.errors()
    assert [e["loc"] for e in errors] == [(field,)]
    if message is not None:
        assert message in errors[0]["msg"]


# Whole object

def test_valid_postal_code(valid_postal_code):
    assert isinstance(valid_postal_code, PostalCode)
    assert valid_postal_code.postal_code == "2200"
    assert valid_postal_code.town == "København N"


def test_model_dump_round_trip(valid_postal_code):
    assert PostalCode(**valid_postal_code.model_dump()) == valid_postal_code


@pytest.mark.parametrize("field", list(PostalCode.model_fields))
def test_missing_required_field_is_rejected(valid_postal_code_data, field):
    data = {k: v for k, v in valid_postal_code_data.items() if k != field}
    with pytest.raises(ValidationError) as exc_info:
        PostalCode(**data)
    assert [e["loc"] for e in exc_info.value.errors()] == [(field,)]


@pytest.mark.parametrize(
    "field, value",
    [
        pytest.param("postal_code", 2200, id="postal_code-int"),
        pytest.param("postal_code", None, id="postal_code-none"),
        pytest.param("town", 123, id="town-int"),
        pytest.param("town", None, id="town-none"),
    ],
)
def test_wrong_type_is_rejected(valid_postal_code_data, field, value):
    assert_field_rejected(valid_postal_code_data, field, value)


# Postal code

@pytest.mark.parametrize(
    "postal_code",
    [
        pytest.param("2200", id="typical"),
        pytest.param("0800", id="leading-zero"),
    ],
)
def test_valid_postal_code_format(valid_postal_code_data, postal_code):
    result = postal_code_with(valid_postal_code_data, postal_code=postal_code)
    assert result.postal_code == postal_code


@pytest.mark.parametrize(
    "postal_code",
    [
        pytest.param("", id="empty"),
        pytest.param("123", id="one-below-length"),
        pytest.param("22000", id="one-above-length"),
        pytest.param("abcd", id="letters-only"),
        pytest.param("22a0", id="letters-mixed-with-digits"),
        pytest.param("\u0662\u0662\u0660\u0660", id="non-ascii-digits"),
    ],
)
def test_invalid_postal_code_format(valid_postal_code_data, postal_code):
    assert_field_rejected(
        valid_postal_code_data,
        "postal_code",
        postal_code,
        "Postal code must be exactly 4 digits",
    )


# Town

@pytest.mark.parametrize(
    "town",
    [
        pytest.param("Aarhus C", id="ascii"),
        pytest.param("Høje-Taastrup", id="danish-letters"),
    ],
)
def test_valid_town(valid_postal_code_data, town):
    assert postal_code_with(valid_postal_code_data, town=town).town == town


def test_town_accepts_town_name_alias(valid_postal_code_data):
    data = {k: v for k, v in valid_postal_code_data.items() if k != "town"}
    data["town_name"] = "Aarhus C"
    assert PostalCode(**data).town == "Aarhus C"
