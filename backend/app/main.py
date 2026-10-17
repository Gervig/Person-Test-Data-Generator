from fastapi import FastAPI

from app.routes import address, health, person, postal_codes

app = FastAPI(title="Personal Test Data Generator API")

app.include_router(health.router)
app.include_router(postal_codes.router)
app.include_router(address.router)
app.include_router(person.router)
