from datetime import date

from pydantic import BaseModel, Field

class Person(BaseModel):
    first_name: str
    last_name: str
    gender: str # male, female, other
    date_of_birth: date # ddMMyy
    cpr: int # 10 digits, first 8 from date_of_birth: ddMMyy - xxxx
    
class Address(BaseModel):
    street: str
    number: int # a number from 1 to 999 optionally followed by an uppercase letter, ex. 43B
    floot: str # st or a number from 1 to 99