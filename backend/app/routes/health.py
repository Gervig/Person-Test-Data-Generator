from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Personal Test Data Generator API is running!"}
