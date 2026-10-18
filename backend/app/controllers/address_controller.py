from app.dtos.address_dto import AddressDTO
from app.services.address_service import generate_address


def get_address() -> AddressDTO:
    return generate_address()
