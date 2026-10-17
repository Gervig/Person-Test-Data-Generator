import pytest

from app.models.postal_code import PostalCode
from app.models.address import Address


@pytest.fixture
def valid_postal_code():
    return PostalCode(
        postal_code="2200",
        town_name="København N",
    )
    
@pytest.fixture
def valid_address(valid_postal_code):
    return Address(
        street="Guldbergsgade",
        number="29",
        floor="1",
        door="e48",
        postal_code=valid_postal_code,
    )
