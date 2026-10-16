import pytest
from pydantic import ValidationError

from app.models import *

@pytest.mark.parametrize(
    "number",
    ["1", "43", "43B", "999Z"],
)
def test_valid_address_number(number):
    Address(number=number, floor="st", door="th")


@pytest.mark.parametrize(
    "number",
    ["0", "1000", "43BB", "ABC"],
)
def test_invalid_house_number(number):
    with pytest.raises(ValidationError):
        Address(number=number, floor="st", door="th")