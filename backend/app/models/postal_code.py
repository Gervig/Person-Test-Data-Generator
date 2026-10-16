from pydantic import BaseModel, field_validator

class PostalCode(BaseModel):
    postal_code: str
    town_name: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if len(value) != 4 or not value.isdigit():
            raise ValueError("Postal code must be exactly 4 digits")
        return value
    
