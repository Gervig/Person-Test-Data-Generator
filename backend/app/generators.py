from datetime import date, timedelta
import random
import string
from random import Random

from app.data_loader import load_person_names
from app.models.person import ALLOWED_PHONE_PREFIXES

# Pure random generators, no DB calls or DTO mapping.


def random_name(rng: Random | None = None) -> dict[str, str]:
    generator = rng or random
    person = generator.choice(load_person_names())
    return {
        "first_name": person["name"],
        "last_name": person["surname"],
        "gender": person["gender"],
    }


def random_date_of_birth(rng: Random | None = None) -> date:
    generator = rng or random
    start = date(1940, 1, 1)
    end = date.today()
    return start + timedelta(days=generator.randint(0, (end - start).days))


def random_cpr(
    date_of_birth: date,
    gender: str,
    rng: Random | None = None,
) -> str:
    generator = rng or random
    date_part = date_of_birth.strftime("%d%m%y")
    last_digit = generator.choice("02468" if gender == "female" else "13579")
    middle = f"{generator.randint(0, 999):03d}"
    return f"{date_part}{middle}{last_digit}"


def random_phone_number(rng: Random | None = None) -> str:
    generator = rng or random
    prefix = generator.choice(ALLOWED_PHONE_PREFIXES)
    return prefix + "".join(generator.choices(string.digits, k=8 - len(prefix)))


def random_street(rng: Random | None = None) -> str:
    generator = rng or random
    return "".join(generator.choices(string.ascii_letters, k=generator.randint(5, 15)))


def random_number(rng: Random | None = None) -> str:
    generator = rng or random
    number = str(generator.randint(1, 999))
    if generator.random() < 0.25:
        number += generator.choice(string.ascii_uppercase)
    return number


def random_floor(rng: Random | None = None) -> str:
    generator = rng or random
    return generator.choice(["st"] + [str(number) for number in range(1, 100)])


def random_door(rng: Random | None = None) -> str:
    generator = rng or random
    letter = generator.choice(string.ascii_lowercase)
    number = generator.randint(1, 999)
    return generator.choice(
        ["th", "mf", "tv"]
        + [str(number) for number in range(1, 51)]
        + [f"{letter}{number}", f"{letter}-{number}"]
    )
