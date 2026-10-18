from pydantic import BaseModel

from app.models.postal_code import PostalCode


class AddressDTO(BaseModel):
    street: str
    number: str
    floor: str
    door: str
    postal_code: PostalCode
