import pytest
from datetime import date

from app.models.postal_code import PostalCode
from app.models.address import Address
from app.models.person import Person


@pytest.fixture
def valid_postal_code():
    return PostalCode(
        postal_code="2200",
        town="København N",
    )
    
@pytest.fixture
def valid_postal_code_data(valid_postal_code):
    return valid_postal_code.model_dump()
    
@pytest.fixture
def valid_address(valid_postal_code):
    return Address(
        street="Guldbergsgade",
        number="29",
        floor="1",
        door="e48",
        postal_code=valid_postal_code,
    )
    
@pytest.fixture
def valid_address_data(valid_address):
    return valid_address.model_dump()


#TODO: do we need both object and dictionary?
@pytest.fixture
def valid_person(valid_address):
    return Person(
        first_name="John",
        last_name="Doe",
        gender="male",
        date_of_birth=date(1990, 1, 17),
        cpr="1701901234",
        mobile_phone_number="42102030",
        address=valid_address,
    )

# returns a dictionary of valid person data for testing purposes
@pytest.fixture
def valid_person_data(valid_person):
    return valid_person.model_dump()