from fastapi import FastAPI, Query

from app.controllers.address_controller import get_address
from app.controllers.person_controller import (
    generate_cpr,
    generate_cpr_and_name,
    generate_cpr_name_and_birth_date,
    generate_mobile_phone_number,
    generate_name,
    generate_name_and_birth_date,
    generate_person,
    generate_persons,
)
from app.controllers.postal_code_controller import list_postal_codes
from app.views.address_view import AddressView
from app.views.person_view import (
    BulkPersonView,
    CprAndNameView,
    CprNameAndBirthDateView,
    CprView,
    NameAndBirthDateView,
    NameView,
    PersonView,
)

app = FastAPI(title="Personal Test Data Generator API")


@app.get("/")
def home():
    return {"message": "Personal Test Data Generator API is running!"}


@app.get("/postal-codes")
def get_postal_codes():
    return list_postal_codes()


@app.get("/cpr", response_model=CprView)
def get_cpr():
    return generate_cpr()


@app.get("/name", response_model=NameView)
def get_name():
    return generate_name()


@app.get("/name-and-birth-date", response_model=NameAndBirthDateView)
def get_name_and_birth_date():
    return generate_name_and_birth_date()


@app.get("/cpr-and-name", response_model=CprAndNameView)
def get_cpr_and_name():
    return generate_cpr_and_name()


@app.get("/cpr-name-and-birth-date", response_model=CprNameAndBirthDateView)
def get_cpr_name_and_birth_date():
    return generate_cpr_name_and_birth_date()


@app.get("/address", response_model=AddressView)
def get_address_endpoint():
    return get_address()


@app.get("/mobile-phone-number")
def get_mobile_phone_number():
    return {"mobile_phone_number": generate_mobile_phone_number()}


@app.get("/person", response_model=PersonView)
def get_person():
    return generate_person()


@app.get("/persons", response_model=BulkPersonView)
def get_persons(
    count: int = Query(default=2, ge=2, le=100),
):
    return BulkPersonView(persons=generate_persons(count))
