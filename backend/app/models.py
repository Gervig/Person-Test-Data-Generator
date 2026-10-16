from datetime import date

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


class Address(BaseModel):
    street: str
    number: str
    floor: str
    door: str
    postal_code: PostalCode

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

# phone pattern, must start with the following:
"""
It must start by some of the following digit combinations: 
2, 30, 31, 40, 41, 42, 50, 51, 52, 53, 60, 61, 71, 81, 91, 92, 93, 
342, 344-349, 356-357, 359, 362, 365-366, 389, 398, 
431, 441, 462, 466, 468, 472, 474, 476, 478, 485-486, 488-489, 493-496, 498-499, 
542-543, 545, 551-552, 556, 571-574, 577, 579, 584, 586-587, 589, 597-598, 
627, 629, 641, 649, 658, 662-665, 667, 692-694, 697, 
771-772, 782-783, 785-786, 788-789, 
826-827, 829
"""

ALLOWED_PHONE_PREFIXES = (
    "2", "30", "31", "40", "41", "42", "50", "51", "52", "53", "60", "61", "71", "81", "91", "92", "93",
    "342", "344", "345", "346", "347", "348", "349", "356", "357", "359", "362", "365", "366", "389", "398", "431", "441", "462", "466",
    "468", "472", "474", "476", "478", "485", "486", "488", "489", "493", "494", "495", "496", "498", "499", 
    "542", "543", "545", "551", "552", "556", "571", "572", "573", "574", "577", "579", "584", "586", "587", "589", "597", "598",
    "627", "629", "641", "649", "658", "662", "663", "664", "665", "667", "692", "693", "694", "697",
    "771", "772", "782", "783", "785", "786", "788", "789",
    "826", "827", "829"
)

class Person(BaseModel):
    first_name: str
    last_name: str
    gender: str # male, female
    date_of_birth: date # ddMMyy
    cpr: str # 10 digits, first 8 from date_of_birth: ddMMyy - xxxx
    address: Address
    mobile_phone_number: str # 8 digits long

    @field_validator("cpr")
    @classmethod
    def validate_cpr(cls, value: str) -> str:
        if len(value) != 10 or not value.isdigit():
            raise ValueError("CPR number must be exactly 10 digits")
        return value

    @field_validator("mobile_phone_number")
    @classmethod
    def validate_mobile_phone_number(cls, value: str) -> str:
        if len(value) != 8 or not value.isdigit():
            raise ValueError("Mobile phone number must be exactly 8 digits")
        if not value.startswith(ALLOWED_PHONE_PREFIXES):
            raise ValueError("Mobile phone number has an invalid prefix")
        return value
    
