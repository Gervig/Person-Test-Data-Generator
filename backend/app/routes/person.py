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
from app.dtos.person_dto import (
    BulkPersonDTO,
    CprAndNameDTO,
    CprNameAndBirthDateDTO,
    CprDTO,
    NameAndBirthDateDTO,
    NameDTO,
    PersonDTO,
)

router = APIRouter()


@router.get("/cpr", response_model=CprDTO)
def get_cpr():
    return generate_cpr()


@router.get("/name", response_model=NameDTO)
def get_name():
    return generate_name()


@router.get("/name-and-birth-date", response_model=NameAndBirthDateDTO)
def get_name_and_birth_date():
    return generate_name_and_birth_date()


@router.get("/cpr-and-name", response_model=CprAndNameDTO)
def get_cpr_and_name():
    return generate_cpr_and_name()


@router.get("/cpr-name-and-birth-date", response_model=CprNameAndBirthDateDTO)
def get_cpr_name_and_birth_date():
    return generate_cpr_name_and_birth_date()


@router.get("/mobile-phone-number")
def get_mobile_phone_number():
    return {"mobile_phone_number": generate_mobile_phone_number()}


@router.get("/person", response_model=PersonDTO)
def get_person():
    return generate_person()


@router.get("/persons", response_model=BulkPersonDTO)
def get_persons(count: int = Query(default=2, ge=1, le=100)):
    return generate_persons(count)
