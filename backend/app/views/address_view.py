from pydantic import BaseModel

from app.models.postal_code import PostalCode


class AddressView(BaseModel):
    street: str
    number: str
    floor: str
    door: str
    postal_code: PostalCode
