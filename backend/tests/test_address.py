import pytest
from pydantic import ValidationError

from app.models import Address

#TODO: add valid Postal Code with fixture

# Positive tests
@pytest.mark.parametrize(
    "street, number, floor, door",
    [
        ("Guldbergsgade", "29", "1", "e48"),
    ],
)
def test_valid_address(street, number, floor, door):
    Address(street=street, number=number, floor=floor, door=door)
    
# Negative tests
@pytest.mark.parametrize(
    "street, number, floor, door",
    [
        (1234, "hejsa", "#!", "wlc"),
    ],
)
def test_valid_address(street, number, floor, door):
    with pytest.raises(ValidationError):
        Address(street=street, number=number, floor=floor, door=door)

