from pydantic import AliasChoices, BaseModel, Field, field_validator

class PostalCode(BaseModel):
    postal_code: str
    town: str = Field(validation_alias=AliasChoices("town", "town_name"))

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if len(value) != 4 or not value.isdigit():
            raise ValueError("Postal code must be exactly 4 digits")
        return value
