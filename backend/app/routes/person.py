from fastapi import APIRouter, Query

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
from app.views.person_view import (
    BulkPersonView,
    CprAndNameView,
    CprNameAndBirthDateView,
    CprView,
    NameAndBirthDateView,
    NameView,
    PersonView,
)

router = APIRouter()


@router.get("/cpr", response_model=CprView)
def get_cpr():
    return generate_cpr()


@router.get("/name", response_model=NameView)
def get_name():
    return generate_name()


@router.get("/name-and-birth-date", response_model=NameAndBirthDateView)
def get_name_and_birth_date():
    return generate_name_and_birth_date()


@router.get("/cpr-and-name", response_model=CprAndNameView)
def get_cpr_and_name():
    return generate_cpr_and_name()


@router.get("/cpr-name-and-birth-date", response_model=CprNameAndBirthDateView)
def get_cpr_name_and_birth_date():
    return generate_cpr_name_and_birth_date()


@router.get("/mobile-phone-number")
def get_mobile_phone_number():
    return {"mobile_phone_number": generate_mobile_phone_number()}


@router.get("/person", response_model=PersonView)
def get_person():
    return generate_person()


@router.get("/persons", response_model=BulkPersonView)
def get_persons(count: int = Query(default=2, ge=2, le=100)):
    return BulkPersonView(persons=generate_persons(count))
