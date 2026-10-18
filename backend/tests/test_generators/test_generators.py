from datetime import date
from random import Random

from app.generators import (
    random_cpr,
    random_date_of_birth,
    random_door,
    random_floor,
    random_name,
    random_number,
    random_phone_number,
    random_street,
)
from app.models.person import ALLOWED_PHONE_PREFIXES


def test_seeded_generators_are_repeatable() -> None:
    first = Random(42)
    second = Random(42)

    assert random_name(first) == random_name(second)
    assert random_date_of_birth(first) == random_date_of_birth(second)
    assert random_street(first) == random_street(second)
    assert random_number(first) == random_number(second)
    assert random_floor(first) == random_floor(second)
    assert random_door(first) == random_door(second)


def test_cpr_contains_date_and_gender_parity() -> None:
    birth_date = date(1990, 1, 17)

    female_cpr = random_cpr(birth_date, "female", Random(1))
    male_cpr = random_cpr(birth_date, "male", Random(1))

    assert female_cpr[:6] == "170190"
    assert int(female_cpr[-1]) % 2 == 0
    assert int(male_cpr[-1]) % 2 == 1

def test_phone_number_has_valid_length_and_prefix() -> None:
    for seed in range(500):
        phone_number = random_phone_number(Random(seed))
        assert len(phone_number) == 8, seed
        assert phone_number.isdigit(), seed
        assert phone_number.startswith(ALLOWED_PHONE_PREFIXES), seed
        
