from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
from datetime import date

from app.models.address import Address

# phone pattern, must start with the following:
ALLOWED_PHONE_PREFIXES = (
    "2", "30", "31", "40", "41", "42", "50", "51", "52", "53", "60", "61", "71", "81", "91", "92", "93",
    "342", "344", "345", "346", "347", "348", "349", "356", "357", "359", "362", "365", "366", "389", "398", 
    "431", "441", "462", "466", "468", "472", "474", "476", "478", "485", "486", "488", "489", "493", "494", "495", "496", "498", "499", 
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
    cpr: str # 10 digits, first 6 from date_of_birth: ddMMyy - xxxx
    mobile_phone_number: str # 8 digits long
    address: Address
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value:str) -> str:
        if (value != "male" and value != "female"):
            raise ValueError("Gender must be male or female")
        return value

    @field_validator("cpr")
    @classmethod
    def validate_cpr_format(cls, value: str) -> str:
        if len(value) != 10 or not value.isdigit():
            raise ValueError("CPR number must be exactly 10 digits")
        return value
    
    @model_validator(mode="after")
    def validate_cpr_date_of_birth(self):
        date_of_birth = self.date_of_birth
        # python date format YYYY-MM-DD to danish ddMMyy
        expected_date = (
            f"{date_of_birth.day:02d}" #02d for preserving leading zeros
            f"{date_of_birth.month:02d}"
            f"{date_of_birth.year % 100:02d}" # get last 2 digits and preserve leading zeros
        )
        # slice cpr from start to position 6 and compare to expected date
        if self.cpr[:6] != expected_date:
            raise ValueError("CPR date of birth mismatch")

        return self

    @field_validator("mobile_phone_number")
    @classmethod
    def validate_mobile_phone_number(cls, value: str) -> str:
        if len(value) != 8 or not value.isdigit():
            raise ValueError("Mobile phone number must be exactly 8 digits")
        if not value.startswith(ALLOWED_PHONE_PREFIXES):
            raise ValueError("Mobile phone number has an invalid prefix")
        return value
    
