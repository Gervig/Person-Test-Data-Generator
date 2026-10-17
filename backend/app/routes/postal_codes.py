from fastapi import APIRouter

from app.controllers.postal_code_controller import list_postal_codes

router = APIRouter()


@router.get("/postal-codes")
def get_postal_codes():
    return list_postal_codes()
