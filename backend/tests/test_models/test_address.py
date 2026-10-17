import pytest
from pydantic import ValidationError

from app.models.address import Address

#TODO: test each input in its own test function with parametrized partitions

# Positive tests

# Test address fixture works
def test_valid_address(valid_address): # valid_address from fixture in tests/confest.py
    assert isinstance(valid_address, Address)
    assert valid_address.street == "Guldbergsgade"
    assert valid_address.number == "29"
    
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

