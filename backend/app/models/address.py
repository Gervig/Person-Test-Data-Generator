from pydantic import BaseModel, field_serializer, field_validator

from app.models.postal_code import PostalCode

class Address(BaseModel):
    street: str
    number: str
    floor: str
    door: str
    postal_code: PostalCode

    @field_serializer("postal_code")
    def serialize_postal_code(self, value: PostalCode) -> dict[str, str]:
        return {
            "postal_code": value.postal_code,
            "town_name": value.town,
        }

    @field_validator("number")
    @classmethod
    def validate_number(cls, value: str) -> str:
        has_suffix = bool(value) and "A" <= value[-1] <= "Z"
        number = value[:-1] if has_suffix else value
        if (
            not number
            or not number.isdigit()
            or number[0] == "0"
            or int(number) > 999
            or len(value) > 4
        ):
            raise ValueError(
                "Address number must be from 1 to 999, optionally followed by "
                "an uppercase letter"
            )
        return value
    
    @field_validator("floor")
    @classmethod
    def validate_floor(cls, value: str) -> str:
        if value != "st" and (
            not value
            or not value.isdigit()
            or value[0] == "0"
            or int(value) > 99
        ):
            raise ValueError("Address floor must be 'st' or a number from 1 to 99")
        return value

    @field_validator("door")
    @classmethod
    def validate_door(cls, value: str) -> str:
        if value in {"th", "mf", "tv"}:
            return value

        if value.isdigit():
            if value[0] != "0" and 1 <= int(value) <= 50:
                return value
        elif len(value) >= 2 and "a" <= value[0] <= "z":
            suffix = value[1:]
            if suffix.startswith("-"):
                suffix = suffix[1:]
            if 1 <= len(suffix) <= 3 and suffix.isdigit():
                return value

        raise ValueError(
            "Address door must be 'th', 'mf', 'tv', a number from 1 to 50, "
            "or a lowercase letter followed by one to three digits"
        )
