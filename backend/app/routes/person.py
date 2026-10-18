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
from app.models.person import (
    Cpr,
    CprAndName,
    CprNameAndBirthDate,
    Name,
    NameAndBirthDate,
    Person,
    PersonList,
)

router = APIRouter()


@router.get("/cpr", response_model=Cpr)
def get_cpr():
    return generate_cpr()


@router.get("/name", response_model=Name)
def get_name():
    return generate_name()


@router.get("/name-and-birth-date", response_model=NameAndBirthDate)
def get_name_and_birth_date():
    return generate_name_and_birth_date()


@router.get("/cpr-and-name", response_model=CprAndName)
def get_cpr_and_name():
    return generate_cpr_and_name()


@router.get("/cpr-name-and-birth-date", response_model=CprNameAndBirthDate)
def get_cpr_name_and_birth_date():
    return generate_cpr_name_and_birth_date()


@router.get("/mobile-phone-number")
def get_mobile_phone_number():
    return {"mobile_phone_number": generate_mobile_phone_number()}


@router.get("/person", response_model=Person)
def get_person():
    return generate_person()


@router.get("/persons", response_model=PersonList)
def get_persons(count: int = Query(default=2, ge=1, le=100)):
    return generate_persons(count)
