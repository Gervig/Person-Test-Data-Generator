from random import Random

from app import generators
from app.models.address import Address
from app.repositories import postal_code_repository


def create_address(rng: Random | None = None) -> Address:
    return Address(
        street=generators.random_street(rng),
        number=generators.random_number(rng),
        floor=generators.random_floor(rng),
        door=generators.random_door(rng),
        postal_code=postal_code_repository.get_random(),
    )


def generate_address(rng: Random | None = None) -> Address:
    return create_address(rng)
