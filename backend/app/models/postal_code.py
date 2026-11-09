from pydantic import AliasChoices, BaseModel, Field, field_validator

from app.models.validators import is_ascii_digits


class PostalCode(BaseModel):
    postal_code: str
    town: str = Field(validation_alias=AliasChoices("town", "town_name"))

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if len(value) != 4 or not is_ascii_digits(value):
            raise ValueError("Postal code must be exactly 4 digits")
        return value
