import pytest
from pydantic import ValidationError

from app.models.postal_code import PostalCode

#TODO: test each input in its own test function with parametrized partitions

# Positive tests

# Test valid_postal_code fixture works
def test_valid_postal_code(valid_postal_code):
    assert isinstance(valid_postal_code, PostalCode)
    assert valid_postal_code.postal_code == "2200"
    assert valid_postal_code.town_name == "København N"
 
# Negative tests   
@pytest.mark.parametrize(
    "postal_code, town_name",
    [
        (1234, "hejsa"), # rejects postal_code as integer
    ],
)
def test_invalid_postal_code(postal_code, town_name):
    with pytest.raises(ValidationError):
        PostalCode(postal_code=postal_code, town_name=town_name)
  