from fastapi import APIRouter

from app.controllers.address_controller import get_address
from app.models.address import Address

router = APIRouter()


@router.get("/address", response_model=Address)
def get_address_endpoint():
    return get_address()
