import pytest
from pydantic import ValidationError

from app.models import PostalCode

#TODO: add data from addresses.sql in data folder

# Positive tests
@pytest.mark.parametrize(
    "postal_code, town_name",
    [
        (1234, "hejsa"),
    ],
)
def test_valid_postal_code(postal_code, town_name):
    PostalCode(postal_code=postal_code, town_name=town_name)
 
# Negative tests   
@pytest.mark.parametrize(
    "postal_code, town_name",
    [
        ("hejsa", 1234),
    ],
)
def test_invalid_postal_code(postal_code, town_name):
    with pytest.raises(ValidationError):
        PostalCode(postal_code=postal_code, town_name=town_name)
  