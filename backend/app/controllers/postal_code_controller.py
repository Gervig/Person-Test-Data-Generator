from app.dtos.postal_code_dto import PostalCodeDTO
from app.repositories import postal_code_repository


def list_postal_codes() -> list[PostalCodeDTO]:
    return [
        PostalCodeDTO(postal_code=postal_code.postal_code, town=postal_code.town_name)
        for postal_code in postal_code_repository.get_all()
    ]
