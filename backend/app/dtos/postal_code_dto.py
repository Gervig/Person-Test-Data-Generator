from pydantic import BaseModel


class PostalCodeDTO(BaseModel):
    postal_code: str
    town: str
