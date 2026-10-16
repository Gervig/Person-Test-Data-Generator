from datetime import date

from pydantic import BaseModel, Field, field_validator

class PostalCode(BaseModel):
    postal_code: str = Field(pattern=r"^\d{4}$") # 4 digits long
    town_name: str
    
class Address(BaseModel):
    street: str
    number: int # a number from 1 to 999 optionally followed by an uppercase letter, e.g. 43B
    floot: str # st or a number from 1 to 99
    door: str # “th”, “mf”, “tv”, a number from 1 to 50, or a lowercase letter optionally followed by a dash, then followed by one to three numeric digits (e.g., c3, d-14)
    postal_code: PostalCode

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
    cpr: str = Field(pattern=r"^\d{10}$") # 10 digits, first 8 from date_of_birth: ddMMyy - xxxx
    address: Address
    mobile_phone_number: str = Field(pattern=r"^\d{8}$") # 8 digits long

    # validates prefix
    @field_validator("mobile_phone_number")
    @classmethod
    def validate_prefix(cls, value: str) -> str:
        if not value.startswith(ALLOWED_PHONE_PREFIXES):
            raise ValueError("Mobile phone number has an invalid prefix")
        return value
    
