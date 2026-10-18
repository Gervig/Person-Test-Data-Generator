from datetime import date, timedelta
import random
import string

from app.data_loader import load_person_names
from app.database import get_connection
from app.models.address import Address
from app.models.person import ALLOWED_PHONE_PREFIXES, Person
from app.models.postal_code import PostalCode
from app.views.address_view import AddressView
from app.views.person_view import (
    CprAndNameView,
    CprNameAndBirthDateView,
    CprView,
    NameAndBirthDateView,
    NameView,
    PersonView,
)


def _random_name() -> dict[str, str]:
    person = random.choice(load_person_names())
    return {
        "first_name": person["name"],
        "last_name": person["surname"],
        "gender": person["gender"],
    }


def _random_date_of_birth() -> date:
    start = date(1940, 1, 1)
    end = date.today()
    return start + timedelta(days=random.randint(0, (end - start).days))


def _random_cpr(date_of_birth: date, gender: str) -> str:
    date_part = date_of_birth.strftime("%d%m%y")
    last_digit = random.choice("02468" if gender == "female" else "13579")
    middle = f"{random.randint(0, 999):03d}"
    return f"{date_part}{middle}{last_digit}"


def _random_phone_number() -> str:
    prefix = random.choice(ALLOWED_PHONE_PREFIXES)
    return prefix + "".join(random.choices(string.digits, k=8 - len(prefix)))


def _get_random_postal_code() -> PostalCode:
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT cPostalCode, cTownName FROM postal_code ORDER BY cPostalCode"
        )
        rows = cursor.fetchall()
        if not rows:
            raise LookupError("The postal_code table contains no rows.")
        postal_code, town_name = random.choice(rows)
        return PostalCode(
            postal_code=postal_code.strip(),
            town_name=town_name,
        )
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def _create_address() -> Address:
    return Address(
        street="".join(random.choices(string.ascii_letters, k=random.randint(5, 15))),
        number=str(random.randint(1, 999))
        + (random.choice(string.ascii_uppercase) if random.random() < 0.25 else ""),
        floor=random.choice(["st"] + [str(number) for number in range(1, 100)]),
        door=random.choice(
            ["th", "mf", "tv"]
            + [str(number) for number in range(1, 51)]
            + [f"{random.choice(string.ascii_lowercase)}{random.randint(1, 999)}"]
        ),
        postal_code=_get_random_postal_code(),
    )


def generate_address() -> AddressView:
    address = _create_address()
    return AddressView.model_validate(address, from_attributes=True)


def generate_name() -> NameView:
    return NameView(**_random_name())


def generate_name_and_birth_date() -> NameAndBirthDateView:
    name = _random_name()
    return NameAndBirthDateView(
        **name,
        date_of_birth=_random_date_of_birth(),
    )


def generate_cpr() -> CprView:
    name = _random_name()
    date_of_birth = _random_date_of_birth()
    return CprView(cpr=_random_cpr(date_of_birth, name["gender"]))


def generate_cpr_and_name() -> CprAndNameView:
    name = _random_name()
    date_of_birth = _random_date_of_birth()
    return CprAndNameView(**name, cpr=_random_cpr(date_of_birth, name["gender"]))


def generate_cpr_name_and_birth_date() -> CprNameAndBirthDateView:
    name = _random_name()
    date_of_birth = _random_date_of_birth()
    return CprNameAndBirthDateView(
        **name,
        cpr=_random_cpr(date_of_birth, name["gender"]),
        date_of_birth=date_of_birth,
    )


def generate_mobile_phone_number() -> str:
    return _random_phone_number()


def generate_person() -> PersonView:
    name = _random_name()
    date_of_birth = _random_date_of_birth()
    person = Person(
        **name,
        date_of_birth=date_of_birth,
        cpr=_random_cpr(date_of_birth, name["gender"]),
        mobile_phone_number=_random_phone_number(),
        address=_create_address(),
    )
    return PersonView.model_validate(person, from_attributes=True)


def generate_persons(count: int) -> list[PersonView]:
    return [generate_person() for _ in range(count)]
