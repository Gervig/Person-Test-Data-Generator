import pytest
from pydantic import ValidationError

from app.models.address import Address

#TODO: setup partitions

# Positive tests
@pytest.mark.parametrize(
    "street, number, floor, door",
    [
        ("Guldbergsgade", "29", "1", "e48"),
    ],
)
def test_valid_address(street, number, floor, door, valid_postal_code): # valid_postal_code from fixture in tests/conftest.py
    Address(street=street, number=number, floor=floor, door=door, postal_code=valid_postal_code)
    
# Negative tests
@pytest.mark.parametrize(
    "street, number, floor, door",
    [
        (1234, "hejsa", "#!", "wlc"),
    ],
)
def test_invalid_address(street, number, floor, door, valid_postal_code): # valid_postal_code from fixture in tests/conftest.py
    with pytest.raises(ValidationError):
        Address(street=street, number=number, floor=floor, door=door, postal_code=valid_postal_code)

