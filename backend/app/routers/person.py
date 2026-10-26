from fastapi import APIRouter, Query

from app.controllers.person_controller import (
    generate_person,
    generate_persons,
)
from app.models.person_responses import (
    Cpr,
    CprAndName,
    CprNameAndBirthDate,
    Name,
    NameAndBirthDate,
    MobilePhoneNumber,
)

from app.models.person import Person, PersonList


router = APIRouter()


@router.get("/cpr", response_model=Cpr)
def get_cpr():
    return generate_person()


@router.get("/name", response_model=Name)
def get_name():
    return generate_person()


@router.get("/name-and-birth-date", response_model=NameAndBirthDate)
def get_name_and_birth_date():
    return generate_person()


@router.get("/cpr-and-name", response_model=CprAndName)
def get_cpr_and_name():
    return generate_person()


@router.get("/cpr-name-and-birth-date", response_model=CprNameAndBirthDate)
def get_cpr_name_and_birth_date():
    return generate_person()


@router.get("/mobile-phone-number", response_model=MobilePhoneNumber)
def get_mobile_phone_number():
    return generate_person()


@router.get("/person", response_model=Person)
def get_person():
    return generate_person()

@router.get("/persons", response_model=PersonList, summary="Get 2 to 100 persons")
def get_persons(count: int = Query(default=2, ge=2, le=100)):
    return generate_persons(count)