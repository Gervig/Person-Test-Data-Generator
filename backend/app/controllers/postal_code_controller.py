from app.models.postal_code import PostalCode
from app.repositories import postal_code_repository


def list_postal_codes() -> list[PostalCode]:
    return postal_code_repository.get_all()
