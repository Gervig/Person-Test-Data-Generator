from fastapi import APIRouter

from app.controllers.address_controller import get_address
from app.dtos.address_dto import AddressDTO

router = APIRouter()


@router.get("/address", response_model=AddressDTO)
def get_address_endpoint():
    return get_address()
