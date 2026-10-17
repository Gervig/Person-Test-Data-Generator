from fastapi import APIRouter

from app.controllers.address_controller import get_address
from app.views.address_view import AddressView

router = APIRouter()


@router.get("/address", response_model=AddressView)
def get_address_endpoint():
    return get_address()
