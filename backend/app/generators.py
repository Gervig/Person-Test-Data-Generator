import random


def generate_name(persons: list[dict]) -> dict:
    return random.choice(persons)


def generate_address(addresses: list[dict]) -> dict:
    return random.choice(addresses)


def generate_postal_code(postal_code: list[dict]) -> dict:
    return random.choice(postal_code)

