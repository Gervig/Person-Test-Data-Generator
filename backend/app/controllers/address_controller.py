from app.models.address import Address
from app.services.address_service import generate_address


def get_address() -> Address:
    return generate_address()
