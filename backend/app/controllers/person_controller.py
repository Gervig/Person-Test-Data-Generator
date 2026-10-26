from app.models.person import (
    Person,
    PersonList,
)
from app.services import person_service


def generate_person() -> Person:
    return person_service.generate_person()


def generate_persons(count: int) -> PersonList:
    return PersonList(persons=person_service.generate_persons(count))
