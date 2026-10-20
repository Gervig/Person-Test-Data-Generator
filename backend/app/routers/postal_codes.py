from fastapi import APIRouter

from app.controllers.postal_code_controller import list_postal_codes
from app.models.postal_code import PostalCode

router = APIRouter()


@router.get("/postal-codes", response_model=list[PostalCode])
def get_postal_codes():
    return list_postal_codes()
