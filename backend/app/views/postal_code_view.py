from pydantic import BaseModel


class PostalCodeView(BaseModel):
    postal_code: str
    town: str
